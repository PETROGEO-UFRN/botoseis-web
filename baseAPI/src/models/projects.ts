import {
  foreignKey,
  pgTable,
  serial,
  timestamp,
  uuid,
  varchar
} from 'drizzle-orm/pg-core'

import { users } from './users'

export const projects = pgTable(
  'projects_table',
  {
    id: serial('id').primaryKey(),
    name: varchar('name'),
    userId: uuid('userId'),
    createdAt: timestamp('created_at', { withTimezone: true }).defaultNow(),
    // *** set by the services on every update
    modifiedAt: timestamp('modified_at', { withTimezone: true })
  },
  table => [
    foreignKey({
      name: 'FK_users_table_projects_table',
      columns: [table.userId],
      foreignColumns: [users.id]
    }).onDelete('cascade')
  ]
)

export type IProject = typeof projects.$inferSelect
export type INewProject = typeof projects.$inferInsert
