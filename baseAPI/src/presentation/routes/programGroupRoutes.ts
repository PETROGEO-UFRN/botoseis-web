import Router from '@koa/router'
import { z } from 'zod'

import { getRouteId } from '@/presentation/middlewares/validateIdRouteParam'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import {
  ProgramGroupCreateSchema,
  ProgramGroupResponseSchema,
  ProgramGroupUpdateSchema
} from '@/schemas/programSchemas'
import {
  PROGRAM_GROUP_NOT_FOUND,
  programGroupService
} from '@/services/programGroupService'

// *** Program catalog administration, public as on the Flask server
export function programGroupRouterFactory(_props: IRouteFactoryProps) {
  const router = new Router({ prefix: '/programs/groups' })

  router.get('/list', async context => {
    const groups = await programGroupService.listAll()
    context.body = z.array(ProgramGroupResponseSchema).parse(groups)
  })

  router.post(
    '/create',
    validateRequestBody(ProgramGroupCreateSchema),
    async context => {
      const group = await programGroupService.create(context.state.body)
      context.body = ProgramGroupResponseSchema.parse(group)
    }
  )

  router.put(
    '/update/:groupId',
    validateRequestBody(ProgramGroupUpdateSchema),
    async context => {
      const groupId = getRouteId(context, 'groupId', PROGRAM_GROUP_NOT_FOUND)
      const group = await programGroupService.update(
        groupId,
        context.state.body
      )
      context.body = ProgramGroupResponseSchema.parse(group)
    }
  )

  router.delete('/delete/:groupId', async context => {
    const groupId = getRouteId(context, 'groupId', PROGRAM_GROUP_NOT_FOUND)
    context.body = ProgramGroupResponseSchema.parse(
      await programGroupService.delete(groupId)
    )
  })

  return router
}
