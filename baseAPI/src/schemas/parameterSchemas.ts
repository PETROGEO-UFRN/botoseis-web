import { createSelectSchema } from 'drizzle-zod'
import type { z } from 'zod'

import { parameters } from '@/models/index'
import {
  AT_LEAST_ONE_FIELD,
  hasAnyField,
  optionalBoolean,
  optionalString,
  requestBody
} from '@/schemas/commonSchemas'

export const ParameterSchema = createSelectSchema(parameters)

export const ParameterUpdateSchema = requestBody({
  name: optionalString().optional(),
  description: optionalString().optional(),
  example: optionalString().optional(),
  input_type: optionalString().optional(),
  isRequired: optionalBoolean().optional()
}).refine(hasAnyField, { error: AT_LEAST_ONE_FIELD })

export const ParameterResponseSchema = ParameterSchema.transform(parameter => ({
  id: parameter.id,
  name: parameter.name,
  description: parameter.description,
  example: parameter.example,
  input_type: parameter.inputType,
  isRequired: parameter.isRequired
}))

export type IParameterUpdate = z.infer<typeof ParameterUpdateSchema>
