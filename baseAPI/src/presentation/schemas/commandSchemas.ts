import type { z } from 'zod'

import {
  requestBody,
  requiredInteger,
  requiredIntegerList,
  requiredString
} from '@/presentation/schemas/commonSchemas'

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

export type ICommandCreateBody = z.infer<typeof CommandCreateSchema>
export type ICommandUpdateParametersBody = z.infer<
  typeof CommandUpdateParametersSchema
>
export type ICommandsUpdateOrderBody = z.infer<typeof CommandsUpdateOrderSchema>
