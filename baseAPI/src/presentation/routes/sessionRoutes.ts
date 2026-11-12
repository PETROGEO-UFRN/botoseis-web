import Router from '@koa/router'

import { authConfig } from '@/config/auth'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import {
  type ISessionCreateBody,
  SessionCreateSchema
} from '@/presentation/schemas/sessionSchemas'
import { serializeSessionCookie } from '@/presentation/serializers/sessionCookie'
import { sessionService } from '@/services/sessionService'

export function sessionRouterFactory({
  environment = 'development'
}: IRouteFactoryProps) {
  const router = new Router({ prefix: '/session' })

  // *** Logs in, the token travels only in the httpOnly cookie
  router.post('/', validateRequestBody(SessionCreateSchema), async context => {
    const { email, password } = context.request.body as ISessionCreateBody
    const token = await sessionService.create(email, password)

    context.append('Set-Cookie', serializeSessionCookie(token, environment))
    context.body = { message: 'Logged in' }
  })

  router.get('/validate', async context => {
    sessionService.validate(context.cookies.get(authConfig.cookieName))
    context.status = 204
  })

  return router
}
