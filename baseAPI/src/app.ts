import cors from '@koa/cors'
import type Router from '@koa/router'
import Koa from 'koa'
import { koaBody } from 'koa-body'

import { isOriginAllowed } from '@/config/cors'
import { errorHandlerFactory } from '@/presentation/middlewares/errorHandler'
import { lineRouterFactory } from '@/presentation/routes/lineRoutes'
import { projectRouterFactory } from '@/presentation/routes/projectRoutes'
import { sessionRouterFactory } from '@/presentation/routes/sessionRoutes'
import { userRouterFactory } from '@/presentation/routes/userRoutes'

export default function appFactory({
  environment = 'development'
}: IAppFactoryProps) {
  const app = new Koa()

  const routers: Router[] = [
    userRouterFactory({ environment }),
    sessionRouterFactory({ environment }),
    projectRouterFactory({ environment }),
    lineRouterFactory({ environment })
  ]

  app.use(errorHandlerFactory({ environment }))
  app.use(
    cors({
      credentials: true,
      origin: context => {
        const origin = context.get('Origin')
        return isOriginAllowed(origin, environment) ? origin : ''
      }
    })
  )
  // *** multipart is parsed for its text fields only, files are not handled
  app.use(koaBody({ multipart: true }))

  for (const router of routers) {
    app.use(router.routes())
    app.use(router.allowedMethods())
  }

  app.use(async (context, next) => {
    if (context.path === '/health') {
      context.body = { status: 'ok' }
      return
    }
    await next()
  })

  return app
}
