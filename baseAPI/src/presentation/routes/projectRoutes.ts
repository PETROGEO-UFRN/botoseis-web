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
  ProjectCreateSchema,
  ProjectResponseSchema,
  ProjectUpdateSchema
} from '@/schemas/projectSchemas'
import { WorkflowSummarySchema } from '@/schemas/workflowSchemas'
import { projectService } from '@/services/projectService'

export function projectRouterFactory(_props: IRouteFactoryProps) {
  const router = new Router({ prefix: '/project' })
  const requireUser = requireAuthentication()
  const requireProjectOwner = requireAuthentication(
    ownerByRouteParam(projectService.findOwner, 'id')
  )

  router.get('/list', requireUser, async context => {
    const user = getAuthenticatedUser(context)
    const projects = await projectService.listByUserId(user.id)
    context.body = z.array(ProjectResponseSchema).parse(projects)
  })

  router.post(
    '/create',
    validateRequestBody(ProjectCreateSchema),
    requireUser,
    async context => {
      const user = getAuthenticatedUser(context)
      const project = await projectService.create(
        user.id,
        context.state.body.name
      )
      context.body = ProjectResponseSchema.parse(project)
    }
  )

  router.put(
    '/update/:id',
    validateRequestBody(ProjectUpdateSchema),
    requireProjectOwner,
    async context => {
      const id = IdSchema.parse(context.params.id)
      const project = await projectService.updateName(
        id,
        context.state.body.name
      )
      context.body = ProjectResponseSchema.parse(project)
    }
  )

  router.delete('/delete/:id', requireProjectOwner, async context => {
    const id = IdSchema.parse(context.params.id)
    context.body = ProjectResponseSchema.parse(await projectService.delete(id))
  })

  router.get('/root-workflows/list/:id', requireProjectOwner, async context => {
    const id = IdSchema.parse(context.params.id)
    const rootWorkflows = await projectService.listRootWorkflows(id)
    context.body = z.array(WorkflowSummarySchema).parse(rootWorkflows)
  })

  return router
}
