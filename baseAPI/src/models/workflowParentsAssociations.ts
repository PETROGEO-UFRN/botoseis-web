import { foreignKey, integer, pgTable } from 'drizzle-orm/pg-core'

import { datasets } from './datasets'
import { lines } from './lines'
import { projects } from './projects'
import { workflows } from './workflows'

// *** One row per workflow, only one of the parent columns is set
export const workflowParentsAssociations = pgTable(
  'workflow_parents_association_table',
  {
    workflowId: integer('workflowId').primaryKey(),
    lineId: integer('lineId'),
    projectId: integer('projectId'),
    datasetId: integer('datasetId')
  },
  table => [
    foreignKey({
      name: 'FK_workflow_parents_association_table_dataset_table',
      columns: [table.datasetId],
      foreignColumns: [datasets.id]
    }).onDelete('cascade'),
    foreignKey({
      name: 'FK_workflow_parents_association_table_lines_table',
      columns: [table.lineId],
      foreignColumns: [lines.id]
    }).onDelete('cascade'),
    foreignKey({
      name: 'FK_workflow_parents_association_table_projects_table',
      columns: [table.projectId],
      foreignColumns: [projects.id]
    }).onDelete('cascade'),
    foreignKey({
      name: 'FK_workflow_parents_association_table_workflows_table',
      columns: [table.workflowId],
      foreignColumns: [workflows.id]
    }).onDelete('cascade')
  ]
)

export type IWorkflowParentsAssociation =
  typeof workflowParentsAssociations.$inferSelect
export type INewWorkflowParentsAssociation =
  typeof workflowParentsAssociations.$inferInsert
