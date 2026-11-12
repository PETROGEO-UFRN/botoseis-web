import type Koa from 'koa'
import type { ZodType } from 'zod'
import { ValidationError } from '@/errors/ValidationError'
import { toValidationMessages } from '@/presentation/schemas/commonSchemas'

// *** JSON bodies are read as is, form bodies as their text fields
export function getRequestData(context: Koa.Context): unknown {
  const body = context.request.body
  if (context.request.is('json')) return body ?? {}
  if (body && typeof body === 'object' && !Array.isArray(body)) return body
  return {}
}

// *** Unknown fields are dropped; the parsed body is stored on the request
export const validateRequestBody = <T>(schema: ZodType<T>) => {
  return async (context: Koa.Context, next: Koa.Next) => {
    const result = schema.safeParse(getRequestData(context))
    if (!result.success) {
      throw new ValidationError(toValidationMessages(result.error))
    }

    Object.assign(context.request, { body: result.data })
    await next()
  }
}
