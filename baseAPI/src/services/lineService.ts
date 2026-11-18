import { asc, eq, inArray } from 'drizzle-orm'

import database from '@/database/connection'
import { AppError } from '@/errors/AppError'
import {
  type ILine,
  lines,
  workflowParentsAssociations,
  workflows
} from '@/models/index'
import type { IEntityOwner } from '@/presentation/middlewares/requireAuthentication'
import type { ILineWithWorkflows } from '@/schemas/lineSchemas'

async function attachWorkflows(
  executor: IDatabaseExecutor,
  targetLines: ILine[]
): Promise<ILineWithWorkflows[]> {
  if (targetLines.length === 0) return []

  const lineWorkflows = await executor
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
        targetLines.map(line => line.id)
      )
    )
    .orderBy(asc(workflows.id))

  return targetLines.map(line => ({
    ...line,
    workflows: lineWorkflows
      .filter(lineWorkflow => lineWorkflow.lineId === line.id)
      .map(({ id, name }) => ({ id, name }))
  }))
}

export const lineService = {
  async findOwner(lineId: number): Promise<IEntityOwner | undefined> {
    const [lineOwner] = await database
      .select({ ownerEmail: lines.ownerEmail })
      .from(lines)
      .where(eq(lines.id, lineId))
    return lineOwner
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
    const [line] = await database
      .insert(lines)
      .values({ name, projectId, ownerEmail })
      .returning()
    return { ...line, workflows: [] }
  },

  async updateName(lineId: number, name: string): Promise<ILineWithWorkflows> {
    const [line] = await database
      .update(lines)
      .set({ name })
      .where(eq(lines.id, lineId))
      .returning()
    if (!line) throw new AppError('Line does not exist', 404)
    const [lineWithWorkflows] = await attachWorkflows(database, [line])
    return lineWithWorkflows
  },

  // *** Answers the line as it was, workflows included
  async delete(lineId: number): Promise<ILineWithWorkflows> {
    return database.transaction(async transaction => {
      const [line] = await transaction
        .select()
        .from(lines)
        .where(eq(lines.id, lineId))
      if (!line) throw new AppError('Line does not exist', 404)

      const [lineWithWorkflows] = await attachWorkflows(transaction, [line])
      await transaction.delete(lines).where(eq(lines.id, lineId))
      return lineWithWorkflows
    })
  }
}
