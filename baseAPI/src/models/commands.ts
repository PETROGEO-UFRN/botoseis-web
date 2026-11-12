import {
  boolean,
  foreignKey,
  integer,
  pgTable,
  serial,
  text,
  varchar
} from 'drizzle-orm/pg-core'

import { programs } from './programs'
import { users } from './users'
import { workflows } from './workflows'

export const commands = pgTable(
  'commands_table',
  {
    id: serial('id').primaryKey(),
    // *** tells apart commands using the same program on one workflow
    name: varchar('name'),
    // *** stringified JSON
    parameters: text('parameters'),
    workflowId: integer('workflowId'),
    ownerEmail: varchar('owner_email'),
    programId: integer('program_id'),
    isActive: boolean('is_active')
  },
  table => [
    foreignKey({
      name: 'FK_programs_table_commands_table',
      columns: [table.programId],
      foreignColumns: [programs.id]
    }),
    foreignKey({
      name: 'FK_users_table_commands_table',
      columns: [table.ownerEmail],
      foreignColumns: [users.email]
    }),
    foreignKey({
      name: 'FK_workflows_table_commands_table',
      columns: [table.workflowId],
      foreignColumns: [workflows.id]
    }).onDelete('cascade')
  ]
)

export type ICommand = typeof commands.$inferSelect
export type INewCommand = typeof commands.$inferInsert
