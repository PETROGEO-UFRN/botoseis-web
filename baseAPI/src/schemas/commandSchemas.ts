import { createSelectSchema } from 'drizzle-zod'
import type { z } from 'zod'

import { commands } from '@/models/index'
import {
  requestBody,
  requiredInteger,
  requiredIntegerList,
  requiredString
} from '@/schemas/commonSchemas'

export const CommandSchema = createSelectSchema(commands)

export const CommandCreateSchema = requestBody({
  name: requiredString(),
  // *** stringified JSON, kept as sent
  parameters: requiredString(),
  program_id: requiredInteger()
})

export const CommandUpdateParametersSchema = requestBody({
  parameters: requiredString()
})

export const CommandsUpdateOrderSchema = requestBody({
  newOrder: requiredIntegerList()
})

export const CommandResponseSchema = CommandSchema.transform(command => ({
  id: command.id,
  program_id: command.programId,
  workflowId: command.workflowId,
  name: command.name,
  is_active: command.isActive,
  parameters: command.parameters
}))

export type ICommandCreate = z.infer<typeof CommandCreateSchema>
