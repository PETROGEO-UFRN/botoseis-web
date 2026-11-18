import { asc, eq, inArray } from 'drizzle-orm'

import database from '@/database/connection'
import { AppError } from '@/errors/AppError'
import { type IProgramGroup, programGroups, programs } from '@/models/index'
import type {
  IProgramGroupCreate,
  IProgramGroupUpdate,
  IProgramGroupWithPrograms
} from '@/schemas/programSchemas'

export const PROGRAM_GROUP_NOT_FOUND = 'Group does not exist'

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

  async findById(groupId: number): Promise<IProgramGroup | undefined> {
    const [group] = await database
      .select()
      .from(programGroups)
      .where(eq(programGroups.id, groupId))
    return group
  },

  async create(
    groupData: IProgramGroupCreate
  ): Promise<IProgramGroupWithPrograms> {
    const [group] = await database
      .insert(programGroups)
      .values({
        name: groupData.name,
        description: groupData.description || ''
      })
      .returning()
    return { ...group, programs: [] }
  },

  async update(
    groupId: number,
    groupData: IProgramGroupUpdate
  ): Promise<IProgramGroupWithPrograms> {
    const [group] = await database
      .update(programGroups)
      .set(groupData)
      .where(eq(programGroups.id, groupId))
      .returning()
    if (!group) throw new AppError(PROGRAM_GROUP_NOT_FOUND, 404)
    const [groupWithPrograms] = await attachPrograms([group])
    return groupWithPrograms
  },

  // *** Answers the group as it was; its programs stay, without a group, by
  // *** the database foreign key action
  async delete(groupId: number): Promise<IProgramGroupWithPrograms> {
    const group = await programGroupService.findById(groupId)
    if (!group) throw new AppError(PROGRAM_GROUP_NOT_FOUND, 404)
    const [groupWithPrograms] = await attachPrograms([group])

    await database.delete(programGroups).where(eq(programGroups.id, groupId))
    return groupWithPrograms
  }
}
