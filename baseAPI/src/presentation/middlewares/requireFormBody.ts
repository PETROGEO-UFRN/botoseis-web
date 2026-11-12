import type Koa from 'koa'

import { AppError } from '@/errors/AppError'

// *** Routes that will take file uploads only accept form bodies
export const requireFormBody = async (context: Koa.Context, next: Koa.Next) => {
  const body = context.request.body
  const isForm = Boolean(context.request.is('urlencoded', 'multipart'))
  const hasFields =
    body !== null && typeof body === 'object' && Object.keys(body).length > 0

  if (!isForm || !hasFields) {
    throw new AppError('No body, JSON is not accepted for this route', 415)
  }
  await next()
}
