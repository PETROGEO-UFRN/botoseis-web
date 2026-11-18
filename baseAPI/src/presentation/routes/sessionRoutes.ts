import Router from '@koa/router'

import { authConfig } from '@/config/auth'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import { SessionCreateSchema } from '@/schemas/sessionSchemas'
import { sessionService } from '@/services/sessionService'

// *** Built by hand: Koa refuses Secure cookies on plain HTTP connections,
// *** while browsers still accept them from localhost
function createSessionCookie(
  token: string,
  environment: environmentType
): string {
  const sameSite = environment === 'production' ? 'None' : 'Lax'
  return [
    `${authConfig.cookieName}=${token}`,
    'Secure',
    'HttpOnly',
    'Path=/',
    `SameSite=${sameSite}`
  ].join('; ')
}

export function sessionRouterFactory({
  environment = 'development'
}: IRouteFactoryProps) {
  const router = new Router({ prefix: '/session' })

  // *** Logs in, the token travels only in the httpOnly cookie
  router.post('/', validateRequestBody(SessionCreateSchema), async context => {
    const { email, password } = context.state.body
    const token = await sessionService.create(email, password)
    context.append('Set-Cookie', createSessionCookie(token, environment))
    context.body = { message: 'Logged in' }
  })

  router.get('/validate', async context => {
    sessionService.validate(context.cookies.get(authConfig.cookieName))
    context.status = 204
  })

  return router
}
