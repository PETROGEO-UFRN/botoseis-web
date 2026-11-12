import type Koa from 'koa'

import { AppError } from '@/errors/AppError'
import { AuthError } from '@/errors/AuthError'
import { ValidationError } from '@/errors/ValidationError'

const FOREIGN_KEY_VIOLATION = '23503'

function getPostgresErrorCode(error: unknown): string | undefined {
  // *** drizzle wraps driver errors, the code lives on the cause
  const candidates = [error, (error as { cause?: unknown })?.cause]
  for (const candidate of candidates) {
    const code = (candidate as { code?: unknown })?.code
    if (typeof code === 'string') return code
  }
  return undefined
}

// *** Every error becomes a JSON body shaped as { "Error": ... }
export const errorHandlerFactory = ({
  environment = 'development'
}: IMiddlewareFactoryProps) => {
  return async (context: Koa.Context, next: Koa.Next) => {
    try {
      await next()
    } catch (error) {
      if (error instanceof ValidationError) {
        context.status = error.statusCode
        context.body = { Error: error.messages }
        return
      }
      if (error instanceof AuthError) {
        context.status = error.statusCode
        context.body = {
          Error:
            environment === 'development' ? error.message : 'Not authorized'
        }
        return
      }
      if (error instanceof AppError) {
        context.status = error.statusCode
        context.body = { Error: error.message }
        return
      }
      if (getPostgresErrorCode(error) === FOREIGN_KEY_VIOLATION) {
        context.status = 409
        context.body = { Error: 'Entity is still referenced by other records' }
        return
      }

      const status = (error as { status?: unknown }).status
      if (typeof status === 'number' && status >= 400 && status < 500) {
        context.status = status
        context.body = { Error: (error as Error).message }
        return
      }

      console.error(error)
      context.status = 500
      context.body = { Error: 'Internal server error' }
    }
  }
}
