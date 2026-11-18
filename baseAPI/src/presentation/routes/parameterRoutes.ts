import Router from '@koa/router'
import { z } from 'zod'

import { getRouteId } from '@/presentation/middlewares/validateIdRouteParam'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import {
  ParameterResponseSchema,
  ParameterUpdateSchema
} from '@/schemas/parameterSchemas'
import {
  PARAMETER_NOT_FOUND,
  parameterService
} from '@/services/parameterService'
import { PROGRAM_NOT_FOUND } from '@/services/programService'

// *** Program catalog administration, public as on the Flask server
export function parameterRouterFactory(_props: IRouteFactoryProps) {
  const router = new Router({ prefix: '/programs/parameters' })

  router.get('/list/:programId', async context => {
    const programId = getRouteId(context, 'programId', PROGRAM_NOT_FOUND)
    const parameters = await parameterService.listByProgramId(programId)
    context.body = z.array(ParameterResponseSchema).parse(parameters)
  })

  router.post('/create/:programId', async context => {
    const programId = getRouteId(context, 'programId', PROGRAM_NOT_FOUND)
    context.body = ParameterResponseSchema.parse(
      await parameterService.create(programId)
    )
  })

  router.put(
    '/update/:parameterId',
    validateRequestBody(ParameterUpdateSchema),
    async context => {
      const parameterId = getRouteId(
        context,
        'parameterId',
        PARAMETER_NOT_FOUND
      )
      const parameter = await parameterService.update(
        parameterId,
        context.state.body
      )
      context.body = ParameterResponseSchema.parse(parameter)
    }
  )

  router.delete('/delete/:parameterId', async context => {
    const parameterId = getRouteId(context, 'parameterId', PARAMETER_NOT_FOUND)
    context.body = ParameterResponseSchema.parse(
      await parameterService.delete(parameterId)
    )
  })

  return router
}
