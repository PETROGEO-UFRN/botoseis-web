import type { z } from 'zod'

import {
  requestBody,
  requiredString
} from '@/presentation/schemas/commonSchemas'

export const LineCreateSchema = requestBody({
  name: requiredString()
})

export const LineUpdateSchema = LineCreateSchema

export type ILineCreateBody = z.infer<typeof LineCreateSchema>
export type ILineUpdateBody = z.infer<typeof LineUpdateSchema>
