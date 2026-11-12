import {
  foreignKey,
  integer,
  type PgTableExtraConfigValue,
  pgTable,
  serial,
  varchar
} from 'drizzle-orm/pg-core'

import { users } from './users'
import { workflows } from './workflows'

// *** Datasets are produced by running workflows, no route manages them here
export const datasets = pgTable(
  'datasets_table',
  {
    id: serial('id').primaryKey(),
    ownerEmail: varchar('owner_email'),
    originWorkflowId: integer('originWorkflowId')
  },
  // *** explicit return type breaks the workflows / file links type cycle
  (table): PgTableExtraConfigValue[] => [
    foreignKey({
      name: 'FK_users_table_dataset_table',
      columns: [table.ownerEmail],
      foreignColumns: [users.email]
    }),
    foreignKey({
      name: 'FK_workflows_tables_datasets_table',
      columns: [table.originWorkflowId],
      foreignColumns: [workflows.id]
    }).onDelete('cascade')
  ]
)

export type IDataset = typeof datasets.$inferSelect
