import Router from '@koa/router'

import {
  getAuthenticatedUser,
  ownerByRouteParam,
  requireAuthentication
} from '@/presentation/middlewares/requireAuthentication'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import { IdSchema } from '@/schemas/commonSchemas'
import {
  type IWorkflowCreate,
  WorkflowCreateSchema,
  WorkflowFileLinkUpdateSchema,
  WorkflowNameUpdateSchema,
  WorkflowOutputNameUpdateSchema,
  WorkflowPostProcessingResponseSchema,
  WorkflowPostProcessingUpdateSchema,
  WorkflowResponseSchema,
  WorkflowSummarySchema
} from '@/schemas/workflowSchemas'
import { lineService } from '@/services/lineService'
import { projectService } from '@/services/projectService'
import { workflowService } from '@/services/workflowService'

export function workflowRouterFactory(_props: IRouteFactoryProps) {
  const router = new Router({ prefix: '/workflow' })
  const requireWorkflowOwner = (paramName: string) =>
    requireAuthentication(
      ownerByRouteParam(workflowService.findOwner, paramName)
    )

  router.get('/show/:id', requireWorkflowOwner('id'), async context => {
    const id = IdSchema.parse(context.params.id)
    context.body = WorkflowResponseSchema.parse(
      await workflowService.showById(id)
    )
  })

  router.post(
    '/create/:parentId',
    validateRequestBody(WorkflowCreateSchema),
    // *** The parent at the route is a line or a project, as told by
    // *** "parentType"
    requireAuthentication<{ body: IWorkflowCreate }>(context =>
      ownerByRouteParam(
        context.state.body.parentType === 'lineId'
          ? lineService.findOwner
          : projectService.findOwner,
        'parentId'
      )(context)
    ),
    async context => {
      const parentId = IdSchema.parse(context.params.parentId)
      const user = getAuthenticatedUser(context)
      const workflow = await workflowService.create(
        user.email,
        context.state.body,
        parentId
      )
      context.body = WorkflowResponseSchema.parse(workflow)
    }
  )

  router.put(
    '/update/:workflowId/name',
    validateRequestBody(WorkflowNameUpdateSchema),
    requireWorkflowOwner('workflowId'),
    async context => {
      const workflowId = IdSchema.parse(context.params.workflowId)
      const workflow = await workflowService.updateName(
        workflowId,
        context.state.body.name
      )
      context.body = WorkflowSummarySchema.parse(workflow)
    }
  )

  router.put(
    '/update/:workflowId/file',
    validateRequestBody(WorkflowFileLinkUpdateSchema),
    requireWorkflowOwner('workflowId'),
    async context => {
      const workflowId = IdSchema.parse(context.params.workflowId)
      const workflow = await workflowService.updateInputFile(
        workflowId,
        context.state.body.fileLinkId
      )
      context.body = WorkflowResponseSchema.parse(workflow)
    }
  )

  router.put(
    '/update/:workflowId/output-name',
    validateRequestBody(WorkflowOutputNameUpdateSchema),
    requireWorkflowOwner('workflowId'),
    async context => {
      const workflowId = IdSchema.parse(context.params.workflowId)
      const workflow = await workflowService.updateOutputName(
        workflowId,
        context.state.body.outputName
      )
      context.body = WorkflowResponseSchema.parse(workflow)
    }
  )

  router.put(
    '/update/:workflowId/post-processing',
    validateRequestBody(WorkflowPostProcessingUpdateSchema),
    requireWorkflowOwner('workflowId'),
    async context => {
      const workflowId = IdSchema.parse(context.params.workflowId)
      const workflow = await workflowService.updatePostProcessingOptions(
        workflowId,
        context.state.body
      )
      context.body = WorkflowPostProcessingResponseSchema.parse(workflow)
    }
  )

  router.delete('/delete/:id', requireWorkflowOwner('id'), async context => {
    const id = IdSchema.parse(context.params.id)
    context.body = WorkflowResponseSchema.parse(
      await workflowService.delete(id)
    )
  })

  return router
}
