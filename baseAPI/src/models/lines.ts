import {
  foreignKey,
  integer,
  pgTable,
  serial,
  varchar
} from 'drizzle-orm/pg-core'

import { projects } from './projects'
import { users } from './users'

export const lines = pgTable(
  'lines_table',
  {
    id: serial('id').primaryKey(),
    name: varchar('name'),
    projectId: integer('projectId'),
    ownerEmail: varchar('owner_email')
  },
  table => [
    foreignKey({
      name: 'FK_projects_table_lines_table',
      columns: [table.projectId],
      foreignColumns: [projects.id]
    }),
    foreignKey({
      name: 'FK_users_table_lines_table',
      columns: [table.ownerEmail],
      foreignColumns: [users.email]
    })
  ]
)

export type ILine = typeof lines.$inferSelect
export type INewLine = typeof lines.$inferInsert
