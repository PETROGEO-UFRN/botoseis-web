import Router from '@koa/router'

import { getRouteId } from '@/presentation/middlewares/validateIdRouteParam'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import {
  type IParameterUpdateBody,
  ParameterUpdateSchema
} from '@/presentation/schemas/parameterSchemas'
import { serializeParameter } from '@/presentation/serializers/parameterSerializer'
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
    context.body = parameters.map(serializeParameter)
  })

  router.post('/create/:programId', async context => {
    const programId = getRouteId(context, 'programId', PROGRAM_NOT_FOUND)
    context.body = serializeParameter(await parameterService.create(programId))
  })

  router.put(
    '/update/:parameterId',
    validateRequestBody(ParameterUpdateSchema),
    async context => {
      const data = context.request.body as IParameterUpdateBody
      const parameterId = getRouteId(
        context,
        'parameterId',
        PARAMETER_NOT_FOUND
      )
      context.body = serializeParameter(
        await parameterService.update(parameterId, data)
      )
    }
  )

  router.delete('/delete/:parameterId', async context => {
    const parameterId = getRouteId(context, 'parameterId', PARAMETER_NOT_FOUND)
    context.body = serializeParameter(
      await parameterService.delete(parameterId)
    )
  })

  return router
}
