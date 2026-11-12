import {
  foreignKey,
  integer,
  pgTable,
  serial,
  timestamp,
  varchar
} from 'drizzle-orm/pg-core'

import { lines } from './lines'

// *** Line helper files (picks tables and velocity models), managed by the
// *** file routes outside this app
export const helperFileLinks = pgTable(
  'helper_file_link_table',
  {
    id: serial('id').primaryKey(),
    path: varchar('path'),
    dataType: varchar('data_type'),
    lineId: integer('lineId'),
    createdAt: timestamp('created_at', { withTimezone: true }).defaultNow(),
    modifiedAt: timestamp('modified_at', { withTimezone: true })
  },
  table => [
    foreignKey({
      name: 'FK_lines_table_helper_file_link_table',
      columns: [table.lineId],
      foreignColumns: [lines.id]
    }).onDelete('cascade')
  ]
)

export type IHelperFileLink = typeof helperFileLinks.$inferSelect
