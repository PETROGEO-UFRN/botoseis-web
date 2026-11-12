import type { ILineWithWorkflows } from '@/services/lineService'

export function serializeLine(line: ILineWithWorkflows) {
  return {
    id: line.id,
    projectId: line.projectId,
    name: line.name,
    workflows: line.workflows
  }
}
