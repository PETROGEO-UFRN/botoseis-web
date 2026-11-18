import { createSelectSchema } from 'drizzle-zod'
import { z } from 'zod'

import { lines } from '@/models/index'
import { requestBody, requiredString } from '@/schemas/commonSchemas'
import { WorkflowSummarySchema } from '@/schemas/workflowSchemas'

export const LineSchema = createSelectSchema(lines)

export const LineWithWorkflowsSchema = LineSchema.extend({
  workflows: z.array(WorkflowSummarySchema)
})

export const LineCreateSchema = requestBody({
  name: requiredString()
})

export const LineUpdateSchema = LineCreateSchema

export const LineResponseSchema = LineWithWorkflowsSchema.pick({
  id: true,
  projectId: true,
  name: true,
  workflows: true
})

export type ILineWithWorkflows = z.infer<typeof LineWithWorkflowsSchema>
