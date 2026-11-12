import Router from '@koa/router'

import { requireFormBody } from '@/presentation/middlewares/requireFormBody'
import { getRouteId } from '@/presentation/middlewares/validateIdRouteParam'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import {
  type IProgramCreateBody,
  type IProgramUpdateBody,
  ProgramCreateSchema,
  ProgramUpdateSchema
} from '@/presentation/schemas/programSchemas'
import { serializeProgram } from '@/presentation/serializers/programSerializer'
import {
  PROGRAM_GROUP_NOT_FOUND,
  PROGRAM_NOT_FOUND,
  programService
} from '@/services/programService'

// *** Program catalog administration, public as on the Flask server
export function programRouterFactory(_props: IRouteFactoryProps) {
  const router = new Router({ prefix: '/programs' })

  router.get('/list/:groupId', async context => {
    const groupId = getRouteId(context, 'groupId', PROGRAM_GROUP_NOT_FOUND)
    const programs = await programService.listByGroupId(groupId)
    context.body = programs.map(serializeProgram)
  })

  router.post(
    '/create/:groupId',
    validateRequestBody(ProgramCreateSchema),
    requireFormBody,
    async context => {
      const data = context.request.body as IProgramCreateBody
      const groupId = getRouteId(context, 'groupId', PROGRAM_GROUP_NOT_FOUND)
      context.body = serializeProgram(
        await programService.create(groupId, data)
      )
    }
  )

  router.put(
    '/update/:programId',
    validateRequestBody(ProgramUpdateSchema),
    requireFormBody,
    async context => {
      const data = context.request.body as IProgramUpdateBody
      const programId = getRouteId(context, 'programId', PROGRAM_NOT_FOUND)
      context.body = serializeProgram(
        await programService.update(programId, data)
      )
    }
  )

  router.delete('/delete/:programId', async context => {
    const programId = getRouteId(context, 'programId', PROGRAM_NOT_FOUND)
    context.body = serializeProgram(await programService.delete(programId))
  })

  return router
}
