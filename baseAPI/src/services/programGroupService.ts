import { asc, eq, inArray } from 'drizzle-orm'

import database from '@/database/connection'
import { AppError } from '@/errors/AppError'
import {
  type IProgram,
  type IProgramGroup,
  programGroups,
  programs
} from '@/models/index'

export const PROGRAM_GROUP_NOT_FOUND = 'Group does not exist'

export interface IProgramGroupWithPrograms extends IProgramGroup {
  programs: IProgram[]
}

async function attachPrograms(
  groups: IProgramGroup[]
): Promise<IProgramGroupWithPrograms[]> {
  if (groups.length === 0) return []

  const groupPrograms = await database
    .select()
    .from(programs)
    .where(
      inArray(
        programs.groupId,
        groups.map(group => group.id)
      )
    )
    .orderBy(asc(programs.id))

  return groups.map(group => ({
    ...group,
    programs: groupPrograms.filter(program => program.groupId === group.id)
  }))
}

export const programGroupService = {
  async listAll(): Promise<IProgramGroupWithPrograms[]> {
    const groups = await database
      .select()
      .from(programGroups)
      .orderBy(asc(programGroups.id))
    return attachPrograms(groups)
  },

  async findById(id: number): Promise<IProgramGroup | undefined> {
    const [group] = await database
      .select()
      .from(programGroups)
      .where(eq(programGroups.id, id))
    return group
  },

  async create(data: {
    name: string
    description?: string
  }): Promise<IProgramGroupWithPrograms> {
    const [group] = await database
      .insert(programGroups)
      .values({ name: data.name, description: data.description || '' })
      .returning()
    return { ...group, programs: [] }
  },

  async update(
    id: number,
    data: { name?: string; description?: string }
  ): Promise<IProgramGroupWithPrograms> {
    const [group] = await database
      .update(programGroups)
      .set(data)
      .where(eq(programGroups.id, id))
      .returning()
    if (!group) throw new AppError(PROGRAM_GROUP_NOT_FOUND, 404)
    const [groupWithPrograms] = await attachPrograms([group])
    return groupWithPrograms
  },

  // *** Answers the group as it was; its programs stay, without a group, as
  // *** the Flask model relationship does
  async delete(id: number): Promise<IProgramGroupWithPrograms> {
    const group = await programGroupService.findById(id)
    if (!group) throw new AppError(PROGRAM_GROUP_NOT_FOUND, 404)
    const [groupWithPrograms] = await attachPrograms([group])

    await database.transaction(async transaction => {
      await transaction
        .update(programs)
        .set({ groupId: null })
        .where(eq(programs.groupId, id))
      await transaction.delete(programGroups).where(eq(programGroups.id, id))
    })
    return groupWithPrograms
  }
}
