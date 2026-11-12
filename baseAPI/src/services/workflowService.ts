import { eq, inArray } from 'drizzle-orm'

import database, { type ITransaction } from '@/database/connection'
import { AppError } from '@/errors/AppError'
import {
  commands,
  type ICommand,
  type IWorkflow,
  type IWorkflowParentsAssociation,
  lines,
  orderedCommandsLists,
  projects,
  suFileLinks,
  workflowParentsAssociations,
  workflows
} from '@/models/index'
import type { IEntityOwner } from '@/presentation/middlewares/requireAuthentication'
import {
  type IPostProcessingOptions,
  parsePostProcessingOptions,
  stringifyPostProcessingOptions
} from '@/services/postProcessingOptions'

type IDatabaseExecutor = typeof database | ITransaction

export type IWorkflowParentKey = 'projectId' | 'lineId'

export type IWorkflowParentType = 'project' | 'line' | 'dataset' | null

export interface IWorkflowDetails extends IWorkflow {
  commands: ICommand[]
  parentType: IWorkflowParentType
}

function getParentType(
  association: IWorkflowParentsAssociation | undefined
): IWorkflowParentType {
  if (association?.projectId) return 'project'
  if (association?.lineId) return 'line'
  if (association?.datasetId) return 'dataset'
  return null
}

// *** Commands in the order kept by the workflow ordered commands list
export async function getOrderedCommands(
  executor: IDatabaseExecutor,
  workflowId: number
): Promise<ICommand[]> {
  const [orderedList] = await executor
    .select({ commandIds: orderedCommandsLists.commandIds })
    .from(orderedCommandsLists)
    .where(eq(orderedCommandsLists.workflowId, workflowId))
  const commandIds = orderedList?.commandIds ?? []
  if (commandIds.length === 0) return []

  const rows = await executor
    .select()
    .from(commands)
    .where(inArray(commands.id, commandIds))
  const byId = new Map(rows.map(command => [command.id, command]))
  return commandIds.flatMap(id => byId.get(id) ?? [])
}

async function getDetails(
  executor: IDatabaseExecutor,
  workflow: IWorkflow
): Promise<IWorkflowDetails> {
  const [association] = await executor
    .select()
    .from(workflowParentsAssociations)
    .where(eq(workflowParentsAssociations.workflowId, workflow.id))

  return {
    ...workflow,
    commands: await getOrderedCommands(executor, workflow.id),
    parentType: getParentType(association)
  }
}

async function findWorkflow(
  executor: IDatabaseExecutor,
  id: number,
  missingStatus = 404
): Promise<IWorkflow> {
  const [workflow] = await executor
    .select()
    .from(workflows)
    .where(eq(workflows.id, id))
  if (!workflow) throw new AppError('Workflow does not exist', missingStatus)
  return workflow
}

async function validateParent(
  executor: IDatabaseExecutor,
  parentKey: IWorkflowParentKey,
  parentId: number
): Promise<void> {
  if (parentKey === 'lineId') {
    const [line] = await executor
      .select({ id: lines.id })
      .from(lines)
      .where(eq(lines.id, parentId))
    if (!line) throw new AppError('Line does not exist', 409)
    return
  }

  const [project] = await executor
    .select({ id: projects.id })
    .from(projects)
    .where(eq(projects.id, parentId))
  if (!project) throw new AppError('Project does not exist', 409)
}

// *** Keeps letters, digits and - _ ( )
export function sanitizeOutputName(outputName: string): string {
  return outputName.replace(/[^a-zA-Z0-9\-_()]/g, '')
}

export const workflowService = {
  async findOwner(id: number): Promise<IEntityOwner | undefined> {
    const [workflow] = await database
      .select({ ownerEmail: workflows.ownerEmail })
      .from(workflows)
      .where(eq(workflows.id, id))
    return workflow
  },

  async showById(id: number): Promise<IWorkflowDetails> {
    return getDetails(database, await findWorkflow(database, id))
  },

  // *** A workflow always has a parent association and an ordered list
  async create(
    ownerEmail: string | null,
    data: { name: string; parentType: IWorkflowParentKey },
    parentId: number
  ): Promise<IWorkflowDetails> {
    return database.transaction(async transaction => {
      await validateParent(transaction, data.parentType, parentId)

      const [workflow] = await transaction
        .insert(workflows)
        .values({
          name: data.name,
          ownerEmail,
          outputName: '',
          postProcessingOptions: stringifyPostProcessingOptions()
        })
        .returning()

      await transaction
        .insert(workflowParentsAssociations)
        .values({ workflowId: workflow.id, [data.parentType]: parentId })
      await transaction
        .insert(orderedCommandsLists)
        .values({ workflowId: workflow.id, commandIds: [] })

      return getDetails(transaction, workflow)
    })
  },

  async updateName(
    id: number,
    name: string
  ): Promise<Pick<IWorkflow, 'id' | 'name'>> {
    const [workflow] = await database
      .update(workflows)
      .set({ name })
      .where(eq(workflows.id, id))
      .returning({ id: workflows.id, name: workflows.name })
    if (!workflow) throw new AppError('Workflow does not exist', 404)
    return workflow
  },

  async updateInputFile(
    id: number,
    fileLinkId: number
  ): Promise<IWorkflowDetails> {
    await findWorkflow(database, id, 409)

    const [fileLink] = await database
      .select({ id: suFileLinks.id })
      .from(suFileLinks)
      .where(eq(suFileLinks.id, fileLinkId))
    if (!fileLink) throw new AppError('FileLink does not exist', 409)

    const [workflow] = await database
      .update(workflows)
      .set({ inputFileLinkId: fileLink.id })
      .where(eq(workflows.id, id))
      .returning()
    return getDetails(database, workflow)
  },

  async updateOutputName(
    id: number,
    outputName: string
  ): Promise<IWorkflowDetails> {
    const [workflow] = await database
      .update(workflows)
      .set({ outputName: sanitizeOutputName(outputName) })
      .where(eq(workflows.id, id))
      .returning()
    if (!workflow) throw new AppError('Workflow does not exist', 404)
    return getDetails(database, workflow)
  },

  async updatePostProcessingOptions(
    id: number,
    options: IPostProcessingOptions
  ): Promise<{ post_processing_options: Partial<IPostProcessingOptions> }> {
    const [workflow] = await database
      .update(workflows)
      .set({ postProcessingOptions: stringifyPostProcessingOptions(options) })
      .where(eq(workflows.id, id))
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
  async delete(id: number): Promise<IWorkflowDetails> {
    return database.transaction(async transaction => {
      const details = await getDetails(
        transaction,
        await findWorkflow(transaction, id)
      )
      await transaction.delete(workflows).where(eq(workflows.id, id))
      return details
    })
  }
}
