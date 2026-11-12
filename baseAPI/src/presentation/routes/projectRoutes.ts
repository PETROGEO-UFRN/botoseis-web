import Router from '@koa/router'

import {
  getAuthenticatedUser,
  ownerByRouteParam,
  requireAuthentication
} from '@/presentation/middlewares/requireAuthentication'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import { IdSchema } from '@/presentation/schemas/commonSchemas'
import {
  type IProjectCreateBody,
  type IProjectUpdateBody,
  ProjectCreateSchema,
  ProjectUpdateSchema
} from '@/presentation/schemas/projectSchemas'
import { serializeProject } from '@/presentation/serializers/projectSerializer'
import { projectService } from '@/services/projectService'

export function projectRouterFactory(_props: IRouteFactoryProps) {
  const router = new Router({ prefix: '/project' })
  const requireProjectOwner = requireAuthentication(
    ownerByRouteParam(projectService.findOwner, 'id')
  )

  router.get('/list', requireAuthentication(), async context => {
    const user = getAuthenticatedUser(context)
    const projects = await projectService.listByUserId(user.id)
    context.body = projects.map(serializeProject)
  })

  router.post(
    '/create',
    validateRequestBody(ProjectCreateSchema),
    requireAuthentication(),
    async context => {
      const { name } = context.request.body as IProjectCreateBody
      const user = getAuthenticatedUser(context)
      context.body = serializeProject(
        await projectService.create(user.id, name)
      )
    }
  )

  router.put(
    '/update/:id',
    validateRequestBody(ProjectUpdateSchema),
    requireProjectOwner,
    async context => {
      const { name } = context.request.body as IProjectUpdateBody
      const id = IdSchema.parse(context.params.id)
      context.body = serializeProject(await projectService.updateName(id, name))
    }
  )

  router.delete('/delete/:id', requireProjectOwner, async context => {
    const id = IdSchema.parse(context.params.id)
    context.body = serializeProject(await projectService.delete(id))
  })

  router.get('/root-workflows/list/:id', requireProjectOwner, async context => {
    const id = IdSchema.parse(context.params.id)
    context.body = await projectService.listRootWorkflows(id)
  })

  return router
}
