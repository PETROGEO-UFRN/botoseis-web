import { foreignKey, integer, pgTable, serial } from 'drizzle-orm/pg-core'

import { workflows } from './workflows'

// *** One row per workflow; "commandIds" keeps the command order, each item
// *** is an id at commands_table
export const orderedCommandsLists = pgTable(
  'ordered_commands_list_table',
  {
    id: serial('id').primaryKey(),
    workflowId: integer('workflowId'),
    commandIds: integer('commandIds').array()
  },
  table => [
    foreignKey({
      name: 'FK_workflows_table_workflow_commands_list_table',
      columns: [table.workflowId],
      foreignColumns: [workflows.id]
    }).onDelete('cascade')
  ]
)

export type IOrderedCommandsList = typeof orderedCommandsLists.$inferSelect
