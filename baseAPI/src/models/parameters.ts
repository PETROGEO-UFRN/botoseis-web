import {
  boolean,
  foreignKey,
  integer,
  pgTable,
  serial,
  varchar
} from 'drizzle-orm/pg-core'

import { programs } from './programs'

export const parameters = pgTable(
  'parameters_table',
  {
    id: serial('id').primaryKey(),
    name: varchar('name'),
    description: varchar('description'),
    inputType: varchar('input_type'),
    programId: integer('programId'),
    isRequired: boolean('isRequired'),
    example: varchar('example')
  },
  table => [
    foreignKey({
      name: 'FK_programs_table_parameters_table',
      columns: [table.programId],
      foreignColumns: [programs.id]
    })
  ]
)

export type IParameter = typeof parameters.$inferSelect
export type INewParameter = typeof parameters.$inferInsert
