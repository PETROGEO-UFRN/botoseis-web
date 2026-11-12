import { serializeCommand } from '@/presentation/serializers/commandSerializer'
import { parsePostProcessingOptions } from '@/services/postProcessingOptions'
import type { IWorkflowDetails } from '@/services/workflowService'

export function serializeWorkflow(workflow: IWorkflowDetails) {
  return {
    id: workflow.id,
    name: workflow.name,
    input_file_link_id: workflow.inputFileLinkId,
    output_name: workflow.outputName,
    post_processing_options: parsePostProcessingOptions(
      workflow.postProcessingOptions
    ),
    commands: workflow.commands.map(serializeCommand),
    parentType: workflow.parentType
  }
}
