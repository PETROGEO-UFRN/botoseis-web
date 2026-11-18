import type {
  ICommand,
  IWorkflow,
  IWorkflowParentsAssociation
} from '@/models/index'
import type { IWorkflowDetails } from '@/schemas/workflowSchemas'

function getParentType(
  parentAssociation: IWorkflowParentsAssociation | undefined
): IWorkflowDetails['parentType'] {
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
