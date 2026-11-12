import { parsePostProcessingOptions } from '@/factories/postProcessingOptionsFactory'
import type { IWorkflowDetails } from '@/factories/workflowFactory'
import { serializeCommand } from '@/presentation/serializers/commandSerializer'

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
