import { z } from 'zod'

import { requestBody, requiredString } from '@/schemas/commonSchemas'
import { UserSchema } from '@/schemas/userSchemas'

export const SessionCreateSchema = requestBody({
  email: requiredString(),
  password: requiredString()
})

// *** Claims of the session token
export const TokenPayloadSchema = UserSchema.pick({ id: true }).extend({
  name: z.string().nullish(),
  email: z.string().nullish()
})

export type ITokenPayload = z.infer<typeof TokenPayloadSchema>
