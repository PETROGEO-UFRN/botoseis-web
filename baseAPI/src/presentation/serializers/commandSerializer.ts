import type { ICommand } from '@/models/index'

export function serializeCommand(command: ICommand) {
  return {
    id: command.id,
    program_id: command.programId,
    workflowId: command.workflowId,
    name: command.name,
    is_active: command.isActive,
    parameters: command.parameters
  }
}
