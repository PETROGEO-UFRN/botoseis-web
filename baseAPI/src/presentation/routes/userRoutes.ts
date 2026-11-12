import Router from '@koa/router'

import {
  getAuthenticatedUser,
  requireAuthentication
} from '@/presentation/middlewares/requireAuthentication'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import {
  type IUserCreateBody,
  type IUserUpdateBody,
  UserCreateSchema,
  UserUpdateSchema
} from '@/presentation/schemas/userSchemas'
import { serializeUser } from '@/presentation/serializers/userSerializer'
import { userService } from '@/services/userService'

export function userRouterFactory(_props: IRouteFactoryProps) {
  const router = new Router({ prefix: '/user' })

  router.post(
    '/create',
    validateRequestBody(UserCreateSchema),
    async context => {
      const data = context.request.body as IUserCreateBody
      const user = await userService.create(data)
      context.body = serializeUser(user)
    }
  )

  // *** debug/test route, lists every user
  router.get('/list', async context => {
    const users = await userService.listAll()
    context.body = users.map(serializeUser)
  })

  router.put(
    '/update',
    validateRequestBody(UserUpdateSchema),
    requireAuthentication(),
    async context => {
      const { name } = context.request.body as IUserUpdateBody
      const user = getAuthenticatedUser(context)
      context.body = serializeUser(await userService.update(user.id, { name }))
    }
  )

  router.delete('/delete', requireAuthentication(), async context => {
    const user = getAuthenticatedUser(context)
    context.body = serializeUser(await userService.delete(user.id))
  })

  return router
}
