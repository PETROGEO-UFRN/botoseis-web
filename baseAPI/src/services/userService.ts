import { randomUUID } from 'node:crypto'
import { eq } from 'drizzle-orm'

import database from '@/database/connection'
import { AppError } from '@/errors/AppError'
import { type IUser, users } from '@/models/index'
import {
  type IUserCreate,
  type IUserUpdate,
  UserIdSchema
} from '@/schemas/userSchemas'
import { passwordService } from '@/services/passwordService'

export const userService = {
  async listAll(): Promise<IUser[]> {
    return database.select().from(users)
  },

  async findById(userId: string): Promise<IUser | undefined> {
    if (!UserIdSchema.safeParse(userId).success) return undefined
    const [user] = await database
      .select()
      .from(users)
      .where(eq(users.id, userId))
    return user
  },

  async findByEmail(email: string): Promise<IUser | undefined> {
    const [user] = await database
      .select()
      .from(users)
      .where(eq(users.email, email))
    return user
  },

  async create(userData: IUserCreate): Promise<IUser> {
    if (await userService.findByEmail(userData.email)) {
      throw new AppError('Email alredy used')
    }

    const [user] = await database
      .insert(users)
      .values({
        id: randomUUID(),
        name: userData.name,
        email: userData.email,
        password: await passwordService.hash(userData.password)
      })
      .returning()
    return user
  },

  async update(userId: string, userData: IUserUpdate): Promise<IUser> {
    const [user] = await database
      .update(users)
      .set({ name: userData.name })
      .where(eq(users.id, userId))
      .returning()
    if (!user) throw new AppError('User does not exist', 404)
    return user
  },

  // *** Projects and lines go along by the database cascade; a user who still
  // *** owns workflows or commands can not be deleted (409)
  async delete(userId: string): Promise<IUser> {
    const [user] = await database
      .delete(users)
      .where(eq(users.id, userId))
      .returning()
    if (!user) throw new AppError('User does not exist', 404)
    return user
  }
}
