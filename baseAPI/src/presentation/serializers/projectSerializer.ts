import type { IProject } from '@/models/index'
import { toHttpDate } from '@/presentation/serializers/common'

export function serializeProject(project: IProject) {
  return {
    id: project.id,
    userId: project.userId,
    name: project.name,
    created_at: toHttpDate(project.createdAt),
    modified_at: toHttpDate(project.modifiedAt)
  }
}
