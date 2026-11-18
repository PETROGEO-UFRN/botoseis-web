import { DrizzleQueryError } from 'drizzle-orm'
import Koa from 'koa'
import { DatabaseError } from 'pg'

import { AppError } from '@/errors/AppError'
import { AuthError } from '@/errors/AuthError'
import { ValidationError } from '@/errors/ValidationError'

const FOREIGN_KEY_VIOLATION = '23503'

function getPostgresErrorCode(error: unknown): string | undefined {
  // *** drizzle wraps driver errors, the PostgreSQL error is the cause
  const databaseError = error instanceof DrizzleQueryError ? error.cause : error
  return databaseError instanceof DatabaseError ? databaseError.code : undefined
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

      // *** framework errors, such as a malformed JSON body
      if (
        error instanceof Koa.HttpError &&
        error.status >= 400 &&
        error.status < 500
      ) {
        context.status = error.status
        context.body = { Error: error.message }
        return
      }

      console.error(error)
      context.status = 500
      context.body = { Error: 'Internal server error' }
    }
  }
}
