import {
  foreignKey,
  integer,
  type PgTableExtraConfigValue,
  pgTable,
  serial,
  timestamp,
  varchar
} from 'drizzle-orm/pg-core'

import { datasets } from './datasets'
import { projects } from './projects'

// *** Seismic Unix file links, managed by the file routes outside this app
export const suFileLinks = pgTable(
  'su_file_link_table',
  {
    id: serial('id').primaryKey(),
    path: varchar('path'),
    projectId: integer('projectId'),
    datasetId: integer('datasetId'),
    createdAt: timestamp('created_at', { withTimezone: true }).defaultNow(),
    modifiedAt: timestamp('modified_at', { withTimezone: true })
  },
  // *** explicit return type breaks the workflows / file links type cycle
  (table): PgTableExtraConfigValue[] => [
    foreignKey({
      name: 'FK_datasets_table_su_file_link_table',
      columns: [table.datasetId],
      foreignColumns: [datasets.id]
    }).onDelete('cascade'),
    foreignKey({
      name: 'FK_projects_table_su_file_link_table',
      columns: [table.projectId],
      foreignColumns: [projects.id]
    }).onDelete('cascade')
  ]
)

export type ISuFileLink = typeof suFileLinks.$inferSelect
