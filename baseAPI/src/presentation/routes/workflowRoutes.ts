import Router from '@koa/router'

import {
  getAuthenticatedUser,
  type IOwnerLoader,
  ownerByRouteParam,
  requireAuthentication
} from '@/presentation/middlewares/requireAuthentication'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import { IdSchema } from '@/presentation/schemas/commonSchemas'
import {
  type IWorkflowCreateBody,
  type IWorkflowFileLinkUpdateBody,
  type IWorkflowNameUpdateBody,
  type IWorkflowOutputNameUpdateBody,
  type IWorkflowPostProcessingUpdateBody,
  WorkflowCreateSchema,
  WorkflowFileLinkUpdateSchema,
  WorkflowNameUpdateSchema,
  WorkflowOutputNameUpdateSchema,
  WorkflowPostProcessingUpdateSchema
} from '@/presentation/schemas/workflowSchemas'
import { serializeWorkflow } from '@/presentation/serializers/workflowSerializer'
import { lineService } from '@/services/lineService'
import { projectService } from '@/services/projectService'
import { workflowService } from '@/services/workflowService'

// *** The parent at the route is a line or a project, as told by "parentType"
const parentOwner: IOwnerLoader = async context => {
  const { parentType } = context.request.body as IWorkflowCreateBody
  const findOwner =
    parentType === 'lineId' ? lineService.findOwner : projectService.findOwner
  return ownerByRouteParam(findOwner, 'parentId')(context)
}

export function workflowRouterFactory(_props: IRouteFactoryProps) {
  const router = new Router({ prefix: '/workflow' })
  const requireWorkflowOwner = (paramName: string) =>
    requireAuthentication(
      ownerByRouteParam(workflowService.findOwner, paramName)
    )

  router.get('/show/:id', requireWorkflowOwner('id'), async context => {
    const id = IdSchema.parse(context.params.id)
    context.body = serializeWorkflow(await workflowService.showById(id))
  })

  router.post(
    '/create/:parentId',
    validateRequestBody(WorkflowCreateSchema),
    requireAuthentication(parentOwner),
    async context => {
      const data = context.request.body as IWorkflowCreateBody
      const parentId = IdSchema.parse(context.params.parentId)
      const user = getAuthenticatedUser(context)
      const workflow = await workflowService.create(user.email, data, parentId)
      context.body = serializeWorkflow(workflow)
    }
  )

  router.put(
    '/update/:workflowId/name',
    validateRequestBody(WorkflowNameUpdateSchema),
    requireWorkflowOwner('workflowId'),
    async context => {
      const { name } = context.request.body as IWorkflowNameUpdateBody
      const workflowId = IdSchema.parse(context.params.workflowId)
      context.body = await workflowService.updateName(workflowId, name)
    }
  )

  router.put(
    '/update/:workflowId/file',
    validateRequestBody(WorkflowFileLinkUpdateSchema),
    requireWorkflowOwner('workflowId'),
    async context => {
      const { fileLinkId } = context.request.body as IWorkflowFileLinkUpdateBody
      const workflowId = IdSchema.parse(context.params.workflowId)
      const workflow = await workflowService.updateInputFile(
        workflowId,
        fileLinkId
      )
      context.body = serializeWorkflow(workflow)
    }
  )

  router.put(
    '/update/:workflowId/output-name',
    validateRequestBody(WorkflowOutputNameUpdateSchema),
    requireWorkflowOwner('workflowId'),
    async context => {
      const { outputName } = context.request
        .body as IWorkflowOutputNameUpdateBody
      const workflowId = IdSchema.parse(context.params.workflowId)
      const workflow = await workflowService.updateOutputName(
        workflowId,
        outputName
      )
      context.body = serializeWorkflow(workflow)
    }
  )

  router.put(
    '/update/:workflowId/post-processing',
    validateRequestBody(WorkflowPostProcessingUpdateSchema),
    requireWorkflowOwner('workflowId'),
    async context => {
      const options = context.request.body as IWorkflowPostProcessingUpdateBody
      const workflowId = IdSchema.parse(context.params.workflowId)
      context.body = await workflowService.updatePostProcessingOptions(
        workflowId,
        options
      )
    }
  )

  router.delete('/delete/:id', requireWorkflowOwner('id'), async context => {
    const id = IdSchema.parse(context.params.id)
    context.body = serializeWorkflow(await workflowService.delete(id))
  })

  return router
}
