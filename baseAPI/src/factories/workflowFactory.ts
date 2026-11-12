import type {
  ICommand,
  IWorkflow,
  IWorkflowParentsAssociation
} from '@/models/index'

export type IWorkflowParentKey = 'projectId' | 'lineId'

export type IWorkflowParentType = 'project' | 'line' | 'dataset' | null

export interface IWorkflowDetails extends IWorkflow {
  commands: ICommand[]
  parentType: IWorkflowParentType
}

function getParentType(
  parentAssociation: IWorkflowParentsAssociation | undefined
): IWorkflowParentType {
  if (parentAssociation?.projectId) return 'project'
  if (parentAssociation?.lineId) return 'line'
  if (parentAssociation?.datasetId) return 'dataset'
  return null
}

// *** The workflow with its ordered commands and parent type
export function createWorkflowDetails(
  workflow: IWorkflow,
  parentAssociation: IWorkflowParentsAssociation | undefined,
  orderedCommands: ICommand[]
): IWorkflowDetails {
  return {
    ...workflow,
    commands: orderedCommands,
    parentType: getParentType(parentAssociation)
  }
}

// *** Keeps letters, digits and - _ ( )
export function createOutputName(outputName: string): string {
  return outputName.replace(/[^a-zA-Z0-9\-_()]/g, '')
}
