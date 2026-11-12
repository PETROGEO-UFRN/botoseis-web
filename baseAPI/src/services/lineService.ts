import { asc, eq, inArray } from 'drizzle-orm'

import database, { type ITransaction } from '@/database/connection'
import { AppError } from '@/errors/AppError'
import {
  type ILine,
  lines,
  projects,
  workflowParentsAssociations,
  workflows
} from '@/models/index'
import type { IEntityOwner } from '@/presentation/middlewares/requireAuthentication'

export interface ILineWithWorkflows extends ILine {
  workflows: { id: number; name: string | null }[]
}

async function attachWorkflows(
  executor: IDatabaseExecutor,
  lineRows: ILine[]
): Promise<ILineWithWorkflows[]> {
  if (lineRows.length === 0) return []

  const rows = await executor
    .select({
      lineId: workflowParentsAssociations.lineId,
      id: workflows.id,
      name: workflows.name
    })
    .from(workflowParentsAssociations)
    .innerJoin(
      workflows,
      eq(workflows.id, workflowParentsAssociations.workflowId)
    )
    .where(
      inArray(
        workflowParentsAssociations.lineId,
        lineRows.map(line => line.id)
      )
    )
    .orderBy(asc(workflows.id))

  return lineRows.map(line => ({
    ...line,
    workflows: rows
      .filter(row => row.lineId === line.id)
      .map(({ id, name }) => ({ id, name }))
  }))
}

type IDatabaseExecutor = typeof database | ITransaction

// *** Same cascade as the Flask models: workflows parented by the lines lose
// *** their parent, helper file links go by the database cascade
export async function removeLines(
  transaction: ITransaction,
  lineIds: number[]
): Promise<ILine[]> {
  if (lineIds.length === 0) return []

  await transaction
    .update(workflowParentsAssociations)
    .set({ lineId: null })
    .where(inArray(workflowParentsAssociations.lineId, lineIds))
  return transaction.delete(lines).where(inArray(lines.id, lineIds)).returning()
}

export const lineService = {
  async findOwner(id: number): Promise<IEntityOwner | undefined> {
    const [line] = await database
      .select({ ownerEmail: lines.ownerEmail })
      .from(lines)
      .where(eq(lines.id, id))
    return line
  },

  async listByProjectId(projectId: number): Promise<ILineWithWorkflows[]> {
    const projectLines = await database
      .select()
      .from(lines)
      .where(eq(lines.projectId, projectId))
      .orderBy(asc(lines.id))
    return attachWorkflows(database, projectLines)
  },

  async create(
    ownerEmail: string | null,
    projectId: number,
    name: string
  ): Promise<ILineWithWorkflows> {
    const [project] = await database
      .select({ id: projects.id })
      .from(projects)
      .where(eq(projects.id, projectId))
    if (!project) throw new AppError('Project does not exist', 404)

    const [line] = await database
      .insert(lines)
      .values({ name, projectId, ownerEmail })
      .returning()
    return { ...line, workflows: [] }
  },

  async updateName(id: number, name: string): Promise<ILineWithWorkflows> {
    const [line] = await database
      .update(lines)
      .set({ name })
      .where(eq(lines.id, id))
      .returning()
    if (!line) throw new AppError('Line does not exist', 404)
    const [lineWithWorkflows] = await attachWorkflows(database, [line])
    return lineWithWorkflows
  },

  // *** Answers the line as it was, workflows included
  async delete(id: number): Promise<ILineWithWorkflows> {
    return database.transaction(async transaction => {
      const [line] = await transaction
        .select()
        .from(lines)
        .where(eq(lines.id, id))
      if (!line) throw new AppError('Line does not exist', 404)

      const [lineWithWorkflows] = await attachWorkflows(transaction, [line])
      await removeLines(transaction, [id])
      return lineWithWorkflows
    })
  }
}
