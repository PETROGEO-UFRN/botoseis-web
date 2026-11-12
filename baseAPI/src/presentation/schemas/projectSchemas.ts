import type { z } from 'zod'

import {
  requestBody,
  requiredString
} from '@/presentation/schemas/commonSchemas'

export const ProjectCreateSchema = requestBody({
  name: requiredString()
})

export const ProjectUpdateSchema = ProjectCreateSchema

export type IProjectCreateBody = z.infer<typeof ProjectCreateSchema>
export type IProjectUpdateBody = z.infer<typeof ProjectUpdateSchema>
