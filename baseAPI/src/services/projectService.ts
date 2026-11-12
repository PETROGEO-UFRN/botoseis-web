import { asc, eq } from 'drizzle-orm'

import database from '@/database/connection'
import { AppError } from '@/errors/AppError'
import {
  type IProject,
  type IWorkflow,
  projects,
  workflowParentsAssociations,
  workflows
} from '@/models/index'
import type { IEntityOwner } from '@/presentation/middlewares/requireAuthentication'

export const projectService = {
  async findOwner(projectId: number): Promise<IEntityOwner | undefined> {
    const [projectOwner] = await database
      .select({ userId: projects.userId })
      .from(projects)
      .where(eq(projects.id, projectId))
    return projectOwner
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

  async updateName(projectId: number, name: string): Promise<IProject> {
    const [project] = await database
      .update(projects)
      .set({ name, modifiedAt: new Date() })
      .where(eq(projects.id, projectId))
      .returning()
    if (!project) throw new AppError('Project does not exist', 404)
    return project
  },

  // *** Lines, workflow associations and file links go by the database cascade
  async delete(projectId: number): Promise<IProject> {
    const [project] = await database
      .delete(projects)
      .where(eq(projects.id, projectId))
      .returning()
    if (!project) throw new AppError('Project does not exist', 404)
    return project
  },

  // *** Workflows attached straight to the project, not the ones in its lines
  async listRootWorkflows(
    projectId: number
  ): Promise<Pick<IWorkflow, 'id' | 'name'>[]> {
    return database
      .select({ id: workflows.id, name: workflows.name })
      .from(workflowParentsAssociations)
      .innerJoin(
        workflows,
        eq(workflows.id, workflowParentsAssociations.workflowId)
      )
      .where(eq(workflowParentsAssociations.projectId, projectId))
      .orderBy(asc(workflows.id))
  }
}
