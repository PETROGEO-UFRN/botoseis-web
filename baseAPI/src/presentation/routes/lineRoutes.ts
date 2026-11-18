import Router from '@koa/router'
import { z } from 'zod'

import {
  getAuthenticatedUser,
  ownerByRouteParam,
  requireAuthentication
} from '@/presentation/middlewares/requireAuthentication'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import { IdSchema } from '@/schemas/commonSchemas'
import {
  LineCreateSchema,
  LineResponseSchema,
  LineUpdateSchema
} from '@/schemas/lineSchemas'
import { lineService } from '@/services/lineService'
import { projectService } from '@/services/projectService'

export function lineRouterFactory(_props: IRouteFactoryProps) {
  const router = new Router({ prefix: '/line' })
  const requireProjectOwner = requireAuthentication(
    ownerByRouteParam(projectService.findOwner, 'projectId')
  )
  const requireLineOwner = requireAuthentication(
    ownerByRouteParam(lineService.findOwner, 'lineId')
  )

  router.get('/list/:projectId', requireProjectOwner, async context => {
    const projectId = IdSchema.parse(context.params.projectId)
    const lines = await lineService.listByProjectId(projectId)
    context.body = z.array(LineResponseSchema).parse(lines)
  })

  router.post(
    '/create/:projectId',
    validateRequestBody(LineCreateSchema),
    requireProjectOwner,
    async context => {
      const projectId = IdSchema.parse(context.params.projectId)
      const user = getAuthenticatedUser(context)
      const line = await lineService.create(
        user.email,
        projectId,
        context.state.body.name
      )
      context.body = LineResponseSchema.parse(line)
    }
  )

  router.put(
    '/update/:lineId',
    validateRequestBody(LineUpdateSchema),
    requireLineOwner,
    async context => {
      const lineId = IdSchema.parse(context.params.lineId)
      const line = await lineService.updateName(lineId, context.state.body.name)
      context.body = LineResponseSchema.parse(line)
    }
  )

  router.delete('/delete/:lineId', requireLineOwner, async context => {
    const lineId = IdSchema.parse(context.params.lineId)
    context.body = LineResponseSchema.parse(await lineService.delete(lineId))
  })

  return router
}
