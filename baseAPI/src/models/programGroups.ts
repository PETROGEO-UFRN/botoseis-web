import { pgTable, serial, varchar } from 'drizzle-orm/pg-core'

export const programGroups = pgTable('program_groups_table', {
  id: serial('id').primaryKey(),
  name: varchar('name'),
  description: varchar('description')
})

export type IProgramGroup = typeof programGroups.$inferSelect
export type INewProgramGroup = typeof programGroups.$inferInsert
