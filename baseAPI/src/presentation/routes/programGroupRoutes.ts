import Router from '@koa/router'

import { getRouteId } from '@/presentation/middlewares/validateIdRouteParam'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import {
  type IProgramGroupCreateBody,
  type IProgramGroupUpdateBody,
  ProgramGroupCreateSchema,
  ProgramGroupUpdateSchema
} from '@/presentation/schemas/programGroupSchemas'
import { serializeProgramGroup } from '@/presentation/serializers/programSerializer'
import {
  PROGRAM_GROUP_NOT_FOUND,
  programGroupService
} from '@/services/programGroupService'

// *** Program catalog administration, public as on the Flask server
export function programGroupRouterFactory(_props: IRouteFactoryProps) {
  const router = new Router({ prefix: '/programs/groups' })

  router.get('/list', async context => {
    const groups = await programGroupService.listAll()
    context.body = groups.map(serializeProgramGroup)
  })

  router.post(
    '/create',
    validateRequestBody(ProgramGroupCreateSchema),
    async context => {
      const data = context.request.body as IProgramGroupCreateBody
      context.body = serializeProgramGroup(
        await programGroupService.create(data)
      )
    }
  )

  router.put(
    '/update/:groupId',
    validateRequestBody(ProgramGroupUpdateSchema),
    async context => {
      const data = context.request.body as IProgramGroupUpdateBody
      const groupId = getRouteId(context, 'groupId', PROGRAM_GROUP_NOT_FOUND)
      context.body = serializeProgramGroup(
        await programGroupService.update(groupId, data)
      )
    }
  )

  router.delete('/delete/:groupId', async context => {
    const groupId = getRouteId(context, 'groupId', PROGRAM_GROUP_NOT_FOUND)
    context.body = serializeProgramGroup(
      await programGroupService.delete(groupId)
    )
  })

  return router
}
