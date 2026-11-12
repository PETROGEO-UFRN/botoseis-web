import { boolean, pgTable, unique, uuid, varchar } from 'drizzle-orm/pg-core'

import { bytea } from './columnTypes'

export const users = pgTable(
  'users_table',
  {
    id: uuid('id').primaryKey(),
    name: varchar('name'),
    email: varchar('email'),
    isAdmin: boolean('is_admin'),
    password: bytea('password')
  },
  table => [unique('users_table_email_key').on(table.email)]
)

export type IUser = typeof users.$inferSelect
export type INewUser = typeof users.$inferInsert
