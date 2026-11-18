import { createSelectSchema } from 'drizzle-zod'
import { z } from 'zod'

import { users } from '@/models/index'
import {
  requestBody,
  requiredEmail,
  requiredString
} from '@/schemas/commonSchemas'

// *** Any 8-4-4-4-12 hex id; the RFC version and variant are not enforced
export const UserIdSchema = z.guid()

export const UserSchema = createSelectSchema(users, { id: UserIdSchema })

export const UserCreateSchema = requestBody({
  name: requiredString(),
  email: requiredEmail(),
  password: requiredString().min(8, { error: 'Invalid Credentials' })
})

export const UserUpdateSchema = requestBody({
  name: requiredString()
})

export const UserResponseSchema = UserSchema.pick({
  id: true,
  name: true,
  email: true
})

export type IUserCreate = z.infer<typeof UserCreateSchema>
export type IUserUpdate = z.infer<typeof UserUpdateSchema>
