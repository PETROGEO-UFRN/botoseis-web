import type { z } from 'zod'

import {
  requestBody,
  requiredString
} from '@/presentation/schemas/commonSchemas'

// *** path_to_executable_file is a plain text field, uploads are not handled
export const ProgramCreateSchema = requestBody({
  name: requiredString(),
  description: requiredString(),
  path_to_executable_file: requiredString()
})

export const ProgramUpdateSchema = ProgramCreateSchema

export type IProgramCreateBody = z.infer<typeof ProgramCreateSchema>
export type IProgramUpdateBody = z.infer<typeof ProgramUpdateSchema>
