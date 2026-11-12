import { randomUUID } from 'node:crypto'
import { eq } from 'drizzle-orm'

import database from '@/database/connection'
import { AppError } from '@/errors/AppError'
import { type IUser, projects, users } from '@/models/index'
import { passwordService } from '@/services/passwordService'
import { removeProjects } from '@/services/projectService'
import { UUID_PATTERN } from '@/services/tokenService'

export const userService = {
  async listAll(): Promise<IUser[]> {
    return database.select().from(users)
  },

  async findById(id: string): Promise<IUser | undefined> {
    if (!UUID_PATTERN.test(id)) return undefined
    const [user] = await database.select().from(users).where(eq(users.id, id))
    return user
  },

  async findByEmail(email: string): Promise<IUser | undefined> {
    const [user] = await database
      .select()
      .from(users)
      .where(eq(users.email, email))
    return user
  },

  async create(data: {
    name: string
    email: string
    password: string
  }): Promise<IUser> {
    if (await userService.findByEmail(data.email)) {
      throw new AppError('Email alredy used')
    }

    const [user] = await database
      .insert(users)
      .values({
        id: randomUUID(),
        name: data.name,
        email: data.email,
        password: await passwordService.hash(data.password)
      })
      .returning()
    return user
  },

  async update(id: string, data: { name: string }): Promise<IUser> {
    const [user] = await database
      .update(users)
      .set({ name: data.name })
      .where(eq(users.id, id))
      .returning()
    if (!user) throw new AppError('User does not exist', 404)
    return user
  },

  // *** Projects go along, with their own cascade
  async delete(id: string): Promise<IUser> {
    const [user] = await database.transaction(async transaction => {
      const userProjects = await transaction
        .select({ id: projects.id })
        .from(projects)
        .where(eq(projects.userId, id))
      await removeProjects(
        transaction,
        userProjects.map(project => project.id)
      )
      return transaction.delete(users).where(eq(users.id, id)).returning()
    })
    if (!user) throw new AppError('User does not exist', 404)
    return user
  }
}
