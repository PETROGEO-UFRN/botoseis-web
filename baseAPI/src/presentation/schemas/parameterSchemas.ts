import type { z } from 'zod'

import {
  AT_LEAST_ONE_FIELD,
  hasAnyField,
  optionalBoolean,
  optionalString,
  requestBody
} from '@/presentation/schemas/commonSchemas'

export const ParameterUpdateSchema = requestBody({
  name: optionalString().optional(),
  description: optionalString().optional(),
  example: optionalString().optional(),
  input_type: optionalString().optional(),
  isRequired: optionalBoolean().optional()
}).refine(hasAnyField, { error: AT_LEAST_ONE_FIELD })

export type IParameterUpdateBody = z.infer<typeof ParameterUpdateSchema>
