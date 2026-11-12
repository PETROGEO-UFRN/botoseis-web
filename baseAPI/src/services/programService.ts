import { asc, eq } from 'drizzle-orm'

import database from '@/database/connection'
import { AppError } from '@/errors/AppError'
import { type IProgram, parameters, programs } from '@/models/index'
import { programGroupService } from '@/services/programGroupService'

export const PROGRAM_NOT_FOUND = 'Program does not exist'
export const PROGRAM_GROUP_NOT_FOUND = 'Program Group does not exist'

export interface IProgramData {
  name: string
  description: string
  path_to_executable_file: string
}

export const programService = {
  async findById(id: number): Promise<IProgram | undefined> {
    const [program] = await database
      .select()
      .from(programs)
      .where(eq(programs.id, id))
    return program
  },

  async listByGroupId(groupId: number): Promise<IProgram[]> {
    if (!(await programGroupService.findById(groupId))) {
      throw new AppError(PROGRAM_GROUP_NOT_FOUND, 404)
    }
    return database
      .select()
      .from(programs)
      .where(eq(programs.groupId, groupId))
      .orderBy(asc(programs.id))
  },

  async create(groupId: number, data: IProgramData): Promise<IProgram> {
    if (!(await programGroupService.findById(groupId))) {
      throw new AppError(PROGRAM_GROUP_NOT_FOUND, 404)
    }
    const [program] = await database
      .insert(programs)
      .values({
        name: data.name,
        description: data.description,
        pathToExecutableFile: data.path_to_executable_file,
        groupId
      })
      .returning()
    return program
  },

  async update(id: number, data: IProgramData): Promise<IProgram> {
    const [program] = await database
      .update(programs)
      .set({
        name: data.name,
        description: data.description,
        pathToExecutableFile: data.path_to_executable_file
      })
      .where(eq(programs.id, id))
      .returning()
    if (!program) throw new AppError(PROGRAM_NOT_FOUND, 404)
    return program
  },

  // *** Parameters belong to the program and go along; programs still used
  // *** by commands can not be deleted (409)
  async delete(id: number): Promise<IProgram> {
    const [program] = await database.transaction(async transaction => {
      await transaction.delete(parameters).where(eq(parameters.programId, id))
      return transaction.delete(programs).where(eq(programs.id, id)).returning()
    })
    if (!program) throw new AppError(PROGRAM_NOT_FOUND, 404)
    return program
  }
}
