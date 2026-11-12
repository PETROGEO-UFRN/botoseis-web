import type { z } from 'zod'

import {
  requestBody,
  requiredEmail,
  requiredString
} from '@/presentation/schemas/commonSchemas'

export const UserUpdateSchema = requestBody({
  name: requiredString()
})

export const UserCreateSchema = requestBody({
  name: requiredString(),
  email: requiredEmail(),
  password: requiredString().min(8, { error: 'Invalid Credentials' })
})

export type IUserCreateBody = z.infer<typeof UserCreateSchema>
export type IUserUpdateBody = z.infer<typeof UserUpdateSchema>
