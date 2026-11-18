import Router from '@koa/router'
import { z } from 'zod'

import {
  getAuthenticatedUser,
  requireAuthentication
} from '@/presentation/middlewares/requireAuthentication'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import {
  UserCreateSchema,
  UserResponseSchema,
  UserUpdateSchema
} from '@/schemas/userSchemas'
import { userService } from '@/services/userService'

export function userRouterFactory(_props: IRouteFactoryProps) {
  const router = new Router({ prefix: '/user' })
  const requireUser = requireAuthentication()

  router.post(
    '/create',
    validateRequestBody(UserCreateSchema),
    async context => {
      const user = await userService.create(context.state.body)
      context.body = UserResponseSchema.parse(user)
    }
  )

  // *** debug/test route, lists every user
  router.get('/list', async context => {
    const users = await userService.listAll()
    context.body = z.array(UserResponseSchema).parse(users)
  })

  router.put(
    '/update',
    validateRequestBody(UserUpdateSchema),
    requireUser,
    async context => {
      const user = getAuthenticatedUser(context)
      const updatedUser = await userService.update(user.id, context.state.body)
      context.body = UserResponseSchema.parse(updatedUser)
    }
  )

  router.delete('/delete', requireUser, async context => {
    const user = getAuthenticatedUser(context)
    context.body = UserResponseSchema.parse(await userService.delete(user.id))
  })

  return router
}
