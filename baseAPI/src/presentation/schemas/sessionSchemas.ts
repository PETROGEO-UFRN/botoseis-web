import type { z } from 'zod'

import {
  requestBody,
  requiredString
} from '@/presentation/schemas/commonSchemas'

export const SessionCreateSchema = requestBody({
  email: requiredString(),
  password: requiredString()
})

export type ISessionCreateBody = z.infer<typeof SessionCreateSchema>
