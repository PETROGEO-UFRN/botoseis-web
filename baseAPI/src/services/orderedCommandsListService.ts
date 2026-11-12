import { eq, inArray } from 'drizzle-orm'

import type { ITransaction } from '@/database/connection'
import { AppError } from '@/errors/AppError'
import {
  commands,
  type ICommand,
  type IOrderedCommandsList,
  orderedCommandsLists
} from '@/models/index'

const ORDERED_LIST_NOT_FOUND = 'OrderedComandsList does not exist'

// *** Every change locks the list row first, so concurrent changes do not lose ids
async function lockList(
  transaction: ITransaction,
  workflowId: number
): Promise<IOrderedCommandsList | undefined> {
  const [orderedCommandsList] = await transaction
    .select()
    .from(orderedCommandsLists)
    .where(eq(orderedCommandsLists.workflowId, workflowId))
    .for('update')
  return orderedCommandsList
}

async function saveList(
  transaction: ITransaction,
  orderedCommandsList: IOrderedCommandsList,
  commandIds: number[]
): Promise<void> {
  await transaction
    .update(orderedCommandsLists)
    .set({ commandIds })
    .where(eq(orderedCommandsLists.id, orderedCommandsList.id))
}

// *** Each workflow has one list keeping the order of its command ids
export const orderedCommandsListService = {
  async create(executor: IDatabaseExecutor, workflowId: number): Promise<void> {
    await executor
      .insert(orderedCommandsLists)
      .values({ workflowId, commandIds: [] })
  },

  // *** Commands in the order kept by the list
  async listCommands(
    executor: IDatabaseExecutor,
    workflowId: number
  ): Promise<ICommand[]> {
    const [orderedCommandsList] = await executor
      .select({ commandIds: orderedCommandsLists.commandIds })
      .from(orderedCommandsLists)
      .where(eq(orderedCommandsLists.workflowId, workflowId))
    const orderedCommandIds = orderedCommandsList?.commandIds ?? []
    if (orderedCommandIds.length === 0) return []

    const workflowCommands = await executor
      .select()
      .from(commands)
      .where(inArray(commands.id, orderedCommandIds))
    const commandsById = new Map(
      workflowCommands.map(command => [command.id, command])
    )
    return orderedCommandIds.flatMap(
      commandId => commandsById.get(commandId) ?? []
    )
  },

  async append(
    transaction: ITransaction,
    workflowId: number,
    commandId: number
  ): Promise<void> {
    const orderedCommandsList = await lockList(transaction, workflowId)
    if (!orderedCommandsList) throw new AppError(ORDERED_LIST_NOT_FOUND)

    await saveList(transaction, orderedCommandsList, [
      ...(orderedCommandsList.commandIds ?? []),
      commandId
    ])
  },

  // *** The new order must hold every current command id exactly once
  async replace(
    transaction: ITransaction,
    workflowId: number,
    requestedCommandIds: number[]
  ): Promise<void> {
    const orderedCommandsList = await lockList(transaction, workflowId)
    if (!orderedCommandsList) throw new AppError(ORDERED_LIST_NOT_FOUND)

    const currentCommandIds = new Set(orderedCommandsList.commandIds ?? [])
    const holdsEveryIdOnce =
      requestedCommandIds.length === currentCommandIds.size &&
      new Set(requestedCommandIds).size === requestedCommandIds.length &&
      requestedCommandIds.every(commandId => currentCommandIds.has(commandId))
    if (!holdsEveryIdOnce) {
      throw new AppError('newOrder must hold exactly the workflow command ids')
    }

    await saveList(transaction, orderedCommandsList, requestedCommandIds)
  },

  // *** A workflow without a list has nothing to remove
  async remove(
    transaction: ITransaction,
    workflowId: number,
    commandId: number
  ): Promise<void> {
    const orderedCommandsList = await lockList(transaction, workflowId)
    if (!orderedCommandsList) return

    await saveList(
      transaction,
      orderedCommandsList,
      (orderedCommandsList.commandIds ?? []).filter(
        orderedCommandId => orderedCommandId !== commandId
      )
    )
  }
}
