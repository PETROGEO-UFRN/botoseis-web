import Router from '@koa/router'

import {
  getAuthenticatedUser,
  ownerByRouteParam,
  requireAuthentication
} from '@/presentation/middlewares/requireAuthentication'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import { IdSchema } from '@/presentation/schemas/commonSchemas'
import {
  type ILineCreateBody,
  type ILineUpdateBody,
  LineCreateSchema,
  LineUpdateSchema
} from '@/presentation/schemas/lineSchemas'
import { serializeLine } from '@/presentation/serializers/lineSerializer'
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
    context.body = lines.map(serializeLine)
  })

  router.post(
    '/create/:projectId',
    validateRequestBody(LineCreateSchema),
    requireProjectOwner,
    async context => {
      const { name } = context.request.body as ILineCreateBody
      const projectId = IdSchema.parse(context.params.projectId)
      const user = getAuthenticatedUser(context)
      const line = await lineService.create(user.email, projectId, name)
      context.body = serializeLine(line)
    }
  )

  router.put(
    '/update/:lineId',
    validateRequestBody(LineUpdateSchema),
    requireLineOwner,
    async context => {
      const { name } = context.request.body as ILineUpdateBody
      const lineId = IdSchema.parse(context.params.lineId)
      context.body = serializeLine(await lineService.updateName(lineId, name))
    }
  )

  router.delete('/delete/:lineId', requireLineOwner, async context => {
    const lineId = IdSchema.parse(context.params.lineId)
    context.body = serializeLine(await lineService.delete(lineId))
  })

  return router
}
