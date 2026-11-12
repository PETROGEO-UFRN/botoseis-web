import {
  foreignKey,
  integer,
  pgTable,
  serial,
  varchar
} from 'drizzle-orm/pg-core'

import { programGroups } from './programGroups'

export const programs = pgTable(
  'programs_table',
  {
    id: serial('id').primaryKey(),
    name: varchar('name'),
    description: varchar('description'),
    // *** executable path or a command available on the shell, such as the
    // *** Seismic Unix programs
    pathToExecutableFile: varchar('path_to_executable_file'),
    groupId: integer('groupId')
  },
  table => [
    foreignKey({
      name: 'FK_program_groups_table_programs_table',
      columns: [table.groupId],
      foreignColumns: [programGroups.id]
    })
  ]
)

export type IProgram = typeof programs.$inferSelect
export type INewProgram = typeof programs.$inferInsert
