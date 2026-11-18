import { createSelectSchema } from 'drizzle-zod'
import { z } from 'zod'

import { workflows } from '@/models/index'
import { CommandResponseSchema, CommandSchema } from '@/schemas/commandSchemas'
import {
  MESSAGES,
  requestBody,
  requiredEnum,
  requiredInteger,
  requiredString
} from '@/schemas/commonSchemas'

// *** No "datasetId": datasets are not created from the routes
export const WORKFLOW_PARENT_KEYS = ['projectId', 'lineId'] as const

// *** Python type names, as reported by the Flask server
function pythonTypeName(value: unknown): string {
  if (value === null) return 'NoneType'
  if (Array.isArray(value)) return 'list'
  if (typeof value === 'object') return 'dict'
  return typeof value
}

export const PostProcessingOptionsSchema = z.object({
  // *** client side program used at the end of the workflow
  key: requiredString(),
  // *** settings for that program, the format depends on the key
  options: z.record(
    z.string(),
    z.union([z.string(), z.number(), z.boolean()], {
      error: issue =>
        `Value for key '${String(issue.path?.at(-1))}' at 'options' must be a primite. Got ${pythonTypeName(issue.input)}.`
    }),
    {
      error: issue =>
        issue.input === undefined ? MESSAGES.required : MESSAGES.mapping
    }
  )
})

export const DEFAULT_POST_PROCESSING_OPTIONS: IPostProcessingOptions = {
  key: 'tab-vizualizer',
  options: {}
}

// *** workflows_table.post_processing_options holds the options as JSON text;
// *** stored values are read as they are, an empty column reads as {}
export const StoredPostProcessingOptionsSchema = z.codec(
  z.string().nullable(),
  PostProcessingOptionsSchema.partial().loose(),
  {
    decode: storedOptions => JSON.parse(storedOptions || '{}'),
    encode: postProcessingOptions => JSON.stringify(postProcessingOptions)
  }
)

export const WorkflowSchema = createSelectSchema(workflows)

export const WorkflowSummarySchema = WorkflowSchema.pick({
  id: true,
  name: true
})

export const WorkflowDetailsSchema = WorkflowSchema.extend({
  commands: z.array(CommandSchema),
  parentType: z.enum(['project', 'line', 'dataset']).nullable()
})

export const WorkflowCreateSchema = requestBody({
  name: requiredString(),
  parentType: requiredEnum(WORKFLOW_PARENT_KEYS)
})

export const WorkflowNameUpdateSchema = requestBody({
  name: requiredString()
})

export const WorkflowFileLinkUpdateSchema = requestBody({
  fileLinkId: requiredInteger()
})

// *** Output names keep letters, digits and - _ ( ) only
export const WorkflowOutputNameUpdateSchema = requestBody({
  outputName: requiredString().transform(outputName =>
    outputName.replace(/[^a-zA-Z0-9\-_()]/g, '')
  )
})

export const WorkflowPostProcessingUpdateSchema = requestBody(
  PostProcessingOptionsSchema.shape
)

export const WorkflowResponseSchema = WorkflowDetailsSchema.extend({
  postProcessingOptions: StoredPostProcessingOptionsSchema,
  commands: z.array(CommandResponseSchema)
}).transform(workflow => ({
  id: workflow.id,
  name: workflow.name,
  input_file_link_id: workflow.inputFileLinkId,
  output_name: workflow.outputName,
  post_processing_options: workflow.postProcessingOptions,
  commands: workflow.commands,
  parentType: workflow.parentType
}))

export const WorkflowPostProcessingResponseSchema = WorkflowSchema.pick({
  postProcessingOptions: true
})
  .extend({ postProcessingOptions: StoredPostProcessingOptionsSchema })
  .transform(workflow => ({
    post_processing_options: workflow.postProcessingOptions
  }))

export type IPostProcessingOptions = z.infer<typeof PostProcessingOptionsSchema>
export type IWorkflowDetails = z.infer<typeof WorkflowDetailsSchema>
export type IWorkflowCreate = z.infer<typeof WorkflowCreateSchema>
