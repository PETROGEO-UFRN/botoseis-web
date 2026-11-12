import type Koa from 'koa'

import { AppError } from '@/errors/AppError'
import { IdSchema } from '@/presentation/schemas/commonSchemas'

// *** Ids that are not positive integers can not match any row
export const validateIdRouteParam = (paramName: string) => {
  return async (context: Koa.Context, next: Koa.Next) => {
    const parsed = IdSchema.safeParse(context.params[paramName])
    if (!parsed.success) {
      throw new AppError('No instance found for this id', 404)
    }

    await next()
  }
}
