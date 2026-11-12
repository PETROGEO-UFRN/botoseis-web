import {
  foreignKey,
  integer,
  type PgTableExtraConfigValue,
  pgTable,
  serial,
  text,
  varchar
} from 'drizzle-orm/pg-core'

import { helperFileLinks } from './helperFileLinks'
import { suFileLinks } from './suFileLinks'
import { users } from './users'

export const workflows = pgTable(
  'workflows_table',
  {
    id: serial('id').primaryKey(),
    name: varchar('name'),
    ownerEmail: varchar('owner_email'),
    outputName: varchar('output_name'),
    inputFileLinkId: integer('input_file_link_id'),
    // *** stringified JSON: { "key": string, "options": object }
    postProcessingOptions: text('post_processing_options'),
    picksTableFileId: integer('picks_table_file_id')
  },
  // *** explicit return type breaks the workflows / file links type cycle
  (table): PgTableExtraConfigValue[] => [
    foreignKey({
      name: 'FK_helper_file_link_table_workflows_table',
      columns: [table.picksTableFileId],
      foreignColumns: [helperFileLinks.id]
    }),
    foreignKey({
      name: 'FK_su_file_links_table_workflows_table',
      columns: [table.inputFileLinkId],
      foreignColumns: [suFileLinks.id]
    }),
    foreignKey({
      name: 'FK_users_table_workflows_table',
      columns: [table.ownerEmail],
      foreignColumns: [users.email]
    })
  ]
)

export type IWorkflow = typeof workflows.$inferSelect
export type INewWorkflow = typeof workflows.$inferInsert
