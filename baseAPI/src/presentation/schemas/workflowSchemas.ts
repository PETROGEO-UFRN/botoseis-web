import { z } from 'zod'

import {
  MESSAGES,
  requestBody,
  requiredEnum,
  requiredInteger,
  requiredString
} from '@/presentation/schemas/commonSchemas'

// *** No "datasetId": datasets are not created from the routes
export const WORKFLOW_PARENT_KEYS = ['projectId', 'lineId'] as const

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

export const WorkflowOutputNameUpdateSchema = requestBody({
  outputName: requiredString()
})

// *** Python type names, as reported by the Flask server
function pythonTypeName(value: unknown): string {
  if (value === null) return 'NoneType'
  if (Array.isArray(value)) return 'list'
  if (typeof value === 'object') return 'dict'
  return typeof value
}

const PostProcessingOptionsSchema = z
  .record(z.string(), z.unknown(), {
    error: issue =>
      issue.input === undefined ? MESSAGES.required : MESSAGES.mapping
  })
  .superRefine((options, context) => {
    for (const [optionKey, value] of Object.entries(options)) {
      if (!['string', 'number', 'boolean'].includes(typeof value)) {
        context.addIssue({
          code: 'custom',
          message: `Value for key '${optionKey}' at 'options' must be a primite. Got ${pythonTypeName(value)}.`
        })
      }
    }
  })
  .transform(options => options as Record<string, string | number | boolean>)

export const WorkflowPostProcessingUpdateSchema = requestBody({
  key: requiredString(),
  options: PostProcessingOptionsSchema
})

export type IWorkflowCreateBody = z.infer<typeof WorkflowCreateSchema>
export type IWorkflowNameUpdateBody = z.infer<typeof WorkflowNameUpdateSchema>
export type IWorkflowFileLinkUpdateBody = z.infer<
  typeof WorkflowFileLinkUpdateSchema
>
export type IWorkflowOutputNameUpdateBody = z.infer<
  typeof WorkflowOutputNameUpdateSchema
>
export type IWorkflowPostProcessingUpdateBody = z.infer<
  typeof WorkflowPostProcessingUpdateSchema
>
