import { asc, eq } from 'drizzle-orm'

import database from '@/database/connection'
import { AppError } from '@/errors/AppError'
import { type IProgram, programs } from '@/models/index'
import type { IProgramData } from '@/schemas/programSchemas'
import { programGroupService } from '@/services/programGroupService'

export const PROGRAM_NOT_FOUND = 'Program does not exist'
export const PROGRAM_GROUP_NOT_FOUND = 'Program Group does not exist'

export const programService = {
  async findById(programId: number): Promise<IProgram | undefined> {
    const [program] = await database
      .select()
      .from(programs)
      .where(eq(programs.id, programId))
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

  async create(groupId: number, programData: IProgramData): Promise<IProgram> {
    if (!(await programGroupService.findById(groupId))) {
      throw new AppError(PROGRAM_GROUP_NOT_FOUND, 404)
    }
    const [program] = await database
      .insert(programs)
      .values({
        name: programData.name,
        description: programData.description,
        pathToExecutableFile: programData.path_to_executable_file,
        groupId
      })
      .returning()
    return program
  },

  async update(
    programId: number,
    programData: IProgramData
  ): Promise<IProgram> {
    const [program] = await database
      .update(programs)
      .set({
        name: programData.name,
        description: programData.description,
        pathToExecutableFile: programData.path_to_executable_file
      })
      .where(eq(programs.id, programId))
      .returning()
    if (!program) throw new AppError(PROGRAM_NOT_FOUND, 404)
    return program
  },

  // *** Parameters go along by the database cascade; programs still used by
  // *** commands can not be deleted (409)
  async delete(programId: number): Promise<IProgram> {
    const [program] = await database
      .delete(programs)
      .where(eq(programs.id, programId))
      .returning()
    if (!program) throw new AppError(PROGRAM_NOT_FOUND, 404)
    return program
  }
}
