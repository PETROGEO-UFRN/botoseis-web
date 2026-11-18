import type { RouterMiddleware } from '@koa/router'
import type Koa from 'koa'
import type { z } from 'zod'

import { ValidationError } from '@/errors/ValidationError'
import { toValidationMessages } from '@/schemas/commonSchemas'

// *** JSON bodies are read as is, form bodies as their text fields
export function getRequestData(context: Koa.Context): unknown {
  const body = context.request.body
  if (context.request.is('json')) return body ?? {}
  if (body && typeof body === 'object' && !Array.isArray(body)) return body
  return {}
}

// *** Unknown fields are dropped; the parsed body goes to context.state.body,
// *** typed by the schema for the rest of the route
export const validateRequestBody =
  <Schema extends z.ZodType>(
    schema: Schema
  ): RouterMiddleware<{ body: z.output<Schema> }> =>
  async (context, next) => {
    const result = schema.safeParse(getRequestData(context))
    if (!result.success) {
      throw new ValidationError(toValidationMessages(result.error))
    }
    context.state.body = result.data
    await next()
  }
