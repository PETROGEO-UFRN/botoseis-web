import Router from '@koa/router'
import { z } from 'zod'

import {
  getAuthenticatedUser,
  ownerByRouteParam,
  requireAuthentication
} from '@/presentation/middlewares/requireAuthentication'
import { validateRequestBody } from '@/presentation/middlewares/validateRequestBody'
import {
  CommandCreateSchema,
  CommandResponseSchema,
  CommandsUpdateOrderSchema,
  CommandUpdateParametersSchema
} from '@/schemas/commandSchemas'
import { IdSchema } from '@/schemas/commonSchemas'
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
    context.body = CommandResponseSchema.parse(await commandService.show(id))
  })

  router.post(
    '/create/:workflowId',
    validateRequestBody(CommandCreateSchema),
    requireWorkflowOwner,
    async context => {
      const workflowId = IdSchema.parse(context.params.workflowId)
      const user = getAuthenticatedUser(context)
      const command = await commandService.create(
        user.email,
        workflowId,
        context.state.body
      )
      context.body = CommandResponseSchema.parse(command)
    }
  )

  router.put(
    '/update/:id/parameters',
    validateRequestBody(CommandUpdateParametersSchema),
    requireCommandOwner,
    async context => {
      const id = IdSchema.parse(context.params.id)
      const command = await commandService.updateParameters(
        id,
        context.state.body.parameters
      )
      context.body = CommandResponseSchema.parse(command)
    }
  )

  router.put('/update/:id/is_active', requireCommandOwner, async context => {
    const id = IdSchema.parse(context.params.id)
    context.body = CommandResponseSchema.parse(
      await commandService.toggleIsActive(id)
    )
  })

  router.put(
    '/order/:workflowId',
    validateRequestBody(CommandsUpdateOrderSchema),
    requireWorkflowOwner,
    async context => {
      const workflowId = IdSchema.parse(context.params.workflowId)
      const orderedCommands = await commandService.updateOrder(
        workflowId,
        context.state.body.newOrder
      )
      context.body = z.array(CommandResponseSchema).parse(orderedCommands)
    }
  )

  router.delete('/delete/:id', requireCommandOwner, async context => {
    const id = IdSchema.parse(context.params.id)
    context.body = CommandResponseSchema.parse(await commandService.delete(id))
  })

  return router
}
