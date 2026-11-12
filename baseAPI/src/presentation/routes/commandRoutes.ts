import Router from '@koa/router'

import {
  getAuthenticatedUser,
  ownerByRouteParam,
  requireAuthentication
} from '@/presentation/middlewares/requireAuthentication'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import {
  CommandCreateSchema,
  CommandsUpdateOrderSchema,
  CommandUpdateParametersSchema,
  type ICommandCreateBody,
  type ICommandsUpdateOrderBody,
  type ICommandUpdateParametersBody
} from '@/presentation/schemas/commandSchemas'
import { IdSchema } from '@/presentation/schemas/commonSchemas'
import { serializeCommand } from '@/presentation/serializers/commandSerializer'
import { commandService } from '@/services/commandService'
import { workflowService } from '@/services/workflowService'

export function commandRouterFactory(_props: IRouteFactoryProps) {
  const router = new Router({ prefix: '/command' })
  const requireCommandOwner = requireAuthentication(
    ownerByRouteParam(commandService.findOwner, 'id')
  )
  const requireWorkflowOwner = requireAuthentication(
    ownerByRouteParam(workflowService.findOwner, 'workflowId')
  )

  router.get('/show/:id', requireCommandOwner, async context => {
    const id = IdSchema.parse(context.params.id)
    context.body = serializeCommand(await commandService.show(id))
  })

  router.post(
    '/create/:workflowId',
    validateRequestBody(CommandCreateSchema),
    requireWorkflowOwner,
    async context => {
      const data = context.request.body as ICommandCreateBody
      const workflowId = IdSchema.parse(context.params.workflowId)
      const user = getAuthenticatedUser(context)
      const command = await commandService.create(user.email, workflowId, data)
      context.body = serializeCommand(command)
    }
  )

  router.put(
    '/update/:id/parameters',
    validateRequestBody(CommandUpdateParametersSchema),
    requireCommandOwner,
    async context => {
      const { parameters } = context.request
        .body as ICommandUpdateParametersBody
      const id = IdSchema.parse(context.params.id)
      context.body = serializeCommand(
        await commandService.updateParameters(id, parameters)
      )
    }
  )

  router.put('/update/:id/is_active', requireCommandOwner, async context => {
    const id = IdSchema.parse(context.params.id)
    context.body = serializeCommand(await commandService.toggleIsActive(id))
  })

  router.put(
    '/order/:workflowId',
    validateRequestBody(CommandsUpdateOrderSchema),
    requireWorkflowOwner,
    async context => {
      const { newOrder } = context.request.body as ICommandsUpdateOrderBody
      const workflowId = IdSchema.parse(context.params.workflowId)
      const ordered = await commandService.updateOrder(workflowId, newOrder)
      context.body = ordered.map(serializeCommand)
    }
  )

  router.delete('/delete/:id', requireCommandOwner, async context => {
    const id = IdSchema.parse(context.params.id)
    context.body = serializeCommand(await commandService.delete(id))
  })

  return router
}
