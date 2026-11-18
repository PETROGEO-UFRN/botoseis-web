import Router from '@koa/router'
import { z } from 'zod'

import { requireFormBody } from '@/presentation/middlewares/requireFormBody'
import { getRouteId } from '@/presentation/middlewares/validateIdRouteParam'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import {
  ProgramCreateSchema,
  ProgramResponseSchema,
  ProgramUpdateSchema
} from '@/schemas/programSchemas'
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
    context.body = z.array(ProgramResponseSchema).parse(programs)
  })

  router.post(
    '/create/:groupId',
    validateRequestBody(ProgramCreateSchema),
    requireFormBody,
    async context => {
      const groupId = getRouteId(context, 'groupId', PROGRAM_GROUP_NOT_FOUND)
      const program = await programService.create(groupId, context.state.body)
      context.body = ProgramResponseSchema.parse(program)
    }
  )

  router.put(
    '/update/:programId',
    validateRequestBody(ProgramUpdateSchema),
    requireFormBody,
    async context => {
      const programId = getRouteId(context, 'programId', PROGRAM_NOT_FOUND)
      const program = await programService.update(programId, context.state.body)
      context.body = ProgramResponseSchema.parse(program)
    }
  )

  router.delete('/delete/:programId', async context => {
    const programId = getRouteId(context, 'programId', PROGRAM_NOT_FOUND)
    context.body = ProgramResponseSchema.parse(
      await programService.delete(programId)
    )
  })

  return router
}
