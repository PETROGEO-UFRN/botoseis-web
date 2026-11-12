import type Koa from 'koa'

import { AppError } from '@/errors/AppError'
import { IdSchema } from '@/presentation/schemas/commonSchemas'

// *** Ids that are not positive integers can not match any row, so they get
// *** the same 404 as a missing entity
export function getRouteId(
  context: Koa.Context,
  paramName: string,
  notFoundMessage = 'No instance found for this id'
): number {
  const parsed = IdSchema.safeParse(context.params[paramName])
  if (!parsed.success) throw new AppError(notFoundMessage, 404)
  return parsed.data
}
