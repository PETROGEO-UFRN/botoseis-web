import type { z } from 'zod'

import {
  AT_LEAST_ONE_FIELD,
  hasAnyField,
  optionalString,
  requestBody,
  requiredString
} from '@/presentation/schemas/commonSchemas'

export const ProgramGroupCreateSchema = requestBody({
  name: requiredString(),
  description: optionalString().optional()
})

export const ProgramGroupUpdateSchema = requestBody({
  name: optionalString().optional(),
  description: optionalString().optional()
}).refine(hasAnyField, { error: AT_LEAST_ONE_FIELD })

export type IProgramGroupCreateBody = z.infer<typeof ProgramGroupCreateSchema>
export type IProgramGroupUpdateBody = z.infer<typeof ProgramGroupUpdateSchema>
