import { asc, eq, inArray } from 'drizzle-orm'

import database, { type ITransaction } from '@/database/connection'
import { AppError } from '@/errors/AppError'
import {
  type IProject,
  type IWorkflow,
  lines,
  projects,
  workflowParentsAssociations,
  workflows
} from '@/models/index'
import type { IEntityOwner } from '@/presentation/middlewares/requireAuthentication'
import { removeLines } from '@/services/lineService'

// *** Same cascade as the Flask models: a project takes its lines along and
// *** line workflows lose their parent; project workflow associations and
// *** file links go by the database cascade
export async function removeProjects(
  transaction: ITransaction,
  projectIds: number[]
): Promise<IProject[]> {
  if (projectIds.length === 0) return []

  const projectLines = await transaction
    .select({ id: lines.id })
    .from(lines)
    .where(inArray(lines.projectId, projectIds))
  await removeLines(
    transaction,
    projectLines.map(line => line.id)
  )

  return transaction
    .delete(projects)
    .where(inArray(projects.id, projectIds))
    .returning()
}

export const projectService = {
  async findOwner(id: number): Promise<IEntityOwner | undefined> {
    const [project] = await database
      .select({ userId: projects.userId })
      .from(projects)
      .where(eq(projects.id, id))
    return project
  },

  async listByUserId(userId: string): Promise<IProject[]> {
    return database
      .select()
      .from(projects)
      .where(eq(projects.userId, userId))
      .orderBy(asc(projects.id))
  },

  async create(userId: string, name: string): Promise<IProject> {
    const [project] = await database
      .insert(projects)
      .values({ name, userId })
      .returning()
    return project
  },

  async updateName(id: number, name: string): Promise<IProject> {
    const [project] = await database
      .update(projects)
      .set({ name, modifiedAt: new Date() })
      .where(eq(projects.id, id))
      .returning()
    if (!project) throw new AppError('Project does not exist', 404)
    return project
  },

  async delete(id: number): Promise<IProject> {
    const [project] = await database.transaction(transaction =>
      removeProjects(transaction, [id])
    )
    if (!project) throw new AppError('Project does not exist', 404)
    return project
  },

  // *** Workflows attached straight to the project, not the ones in its lines
  async listRootWorkflows(
    id: number
  ): Promise<Pick<IWorkflow, 'id' | 'name'>[]> {
    return database
      .select({ id: workflows.id, name: workflows.name })
      .from(workflowParentsAssociations)
      .innerJoin(
        workflows,
        eq(workflows.id, workflowParentsAssociations.workflowId)
      )
      .where(eq(workflowParentsAssociations.projectId, id))
      .orderBy(asc(workflows.id))
  }
}
