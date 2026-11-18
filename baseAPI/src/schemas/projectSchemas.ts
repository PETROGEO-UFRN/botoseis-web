import { createSelectSchema } from 'drizzle-zod'

import { projects } from '@/models/index'
import { requestBody, requiredString } from '@/schemas/commonSchemas'

export const ProjectSchema = createSelectSchema(projects)

export const ProjectCreateSchema = requestBody({
  name: requiredString()
})

export const ProjectUpdateSchema = ProjectCreateSchema

// *** Dates are sent as RFC 1123 strings in GMT, like Flask's jsonify
export const ProjectResponseSchema = ProjectSchema.transform(project => ({
  id: project.id,
  userId: project.userId,
  name: project.name,
  created_at: project.createdAt?.toUTCString() ?? null,
  modified_at: project.modifiedAt?.toUTCString() ?? null
}))
