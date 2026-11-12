import { eq } from 'drizzle-orm'

import database from '@/database/connection'
import { AppError } from '@/errors/AppError'
import {
  createPostProcessingOptions,
  type IPostProcessingOptions,
  parsePostProcessingOptions
} from '@/factories/postProcessingOptionsFactory'
import {
  createOutputName,
  createWorkflowDetails,
  type IWorkflowDetails,
  type IWorkflowParentKey
} from '@/factories/workflowFactory'
import {
  type IWorkflow,
  suFileLinks,
  workflowParentsAssociations,
  workflows
} from '@/models/index'
import type { IEntityOwner } from '@/presentation/middlewares/requireAuthentication'
import { orderedCommandsListService } from '@/services/orderedCommandsListService'

async function getDetails(
  executor: IDatabaseExecutor,
  workflow: IWorkflow
): Promise<IWorkflowDetails> {
  const [parentAssociation] = await executor
    .select()
    .from(workflowParentsAssociations)
    .where(eq(workflowParentsAssociations.workflowId, workflow.id))

  return createWorkflowDetails(
    workflow,
    parentAssociation,
    await orderedCommandsListService.listCommands(executor, workflow.id)
  )
}

async function findWorkflow(
  executor: IDatabaseExecutor,
  workflowId: number
): Promise<IWorkflow> {
  const [workflow] = await executor
    .select()
    .from(workflows)
    .where(eq(workflows.id, workflowId))
  if (!workflow) throw new AppError('Workflow does not exist', 404)
  return workflow
}

export const workflowService = {
  async findOwner(workflowId: number): Promise<IEntityOwner | undefined> {
    const [workflowOwner] = await database
      .select({ ownerEmail: workflows.ownerEmail })
      .from(workflows)
      .where(eq(workflows.id, workflowId))
    return workflowOwner
  },

  async showById(workflowId: number): Promise<IWorkflowDetails> {
    return getDetails(database, await findWorkflow(database, workflowId))
  },

  // *** A workflow always has a parent association and an ordered list
  async create(
    ownerEmail: string | null,
    workflowData: { name: string; parentType: IWorkflowParentKey },
    parentId: number
  ): Promise<IWorkflowDetails> {
    return database.transaction(async transaction => {
      const [workflow] = await transaction
        .insert(workflows)
        .values({
          name: workflowData.name,
          ownerEmail,
          outputName: '',
          postProcessingOptions: createPostProcessingOptions()
        })
        .returning()

      await transaction.insert(workflowParentsAssociations).values({
        workflowId: workflow.id,
        projectId: workflowData.parentType === 'projectId' ? parentId : null,
        lineId: workflowData.parentType === 'lineId' ? parentId : null
      })
      await orderedCommandsListService.create(transaction, workflow.id)

      return getDetails(transaction, workflow)
    })
  },

  async updateName(
    workflowId: number,
    name: string
  ): Promise<Pick<IWorkflow, 'id' | 'name'>> {
    const [workflow] = await database
      .update(workflows)
      .set({ name })
      .where(eq(workflows.id, workflowId))
      .returning({ id: workflows.id, name: workflows.name })
    if (!workflow) throw new AppError('Workflow does not exist', 404)
    return workflow
  },

  async updateInputFile(
    workflowId: number,
    fileLinkId: number
  ): Promise<IWorkflowDetails> {
    const [fileLink] = await database
      .select({ id: suFileLinks.id })
      .from(suFileLinks)
      .where(eq(suFileLinks.id, fileLinkId))
    if (!fileLink) throw new AppError('FileLink does not exist', 409)

    const [workflow] = await database
      .update(workflows)
      .set({ inputFileLinkId: fileLink.id })
      .where(eq(workflows.id, workflowId))
      .returning()
    if (!workflow) throw new AppError('Workflow does not exist', 404)
    return getDetails(database, workflow)
  },

  async updateOutputName(
    workflowId: number,
    outputName: string
  ): Promise<IWorkflowDetails> {
    const [workflow] = await database
      .update(workflows)
      .set({ outputName: createOutputName(outputName) })
      .where(eq(workflows.id, workflowId))
      .returning()
    if (!workflow) throw new AppError('Workflow does not exist', 404)
    return getDetails(database, workflow)
  },

  async updatePostProcessingOptions(
    workflowId: number,
    postProcessingOptions: IPostProcessingOptions
  ): Promise<{ post_processing_options: Partial<IPostProcessingOptions> }> {
    const [workflow] = await database
      .update(workflows)
      .set({
        postProcessingOptions: createPostProcessingOptions(
          postProcessingOptions
        )
      })
      .where(eq(workflows.id, workflowId))
      .returning()
    if (!workflow) throw new AppError('Workflow does not exist', 404)
    return {
      post_processing_options: parsePostProcessingOptions(
        workflow.postProcessingOptions
      )
    }
  },

  // *** Answers the workflow as it was; commands, the ordered list, the parent
  // *** association and datasets go by the database cascade
  async delete(workflowId: number): Promise<IWorkflowDetails> {
    return database.transaction(async transaction => {
      const workflowDetails = await getDetails(
        transaction,
        await findWorkflow(transaction, workflowId)
      )
      await transaction.delete(workflows).where(eq(workflows.id, workflowId))
      return workflowDetails
    })
  }
}
