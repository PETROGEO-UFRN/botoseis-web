import { eq } from 'drizzle-orm'

import database from '@/database/connection'
import { AppError } from '@/errors/AppError'
import {
  commands,
  type ICommand,
  orderedCommandsLists,
  workflows
} from '@/models/index'
import type { IEntityOwner } from '@/presentation/middlewares/requireAuthentication'
import { PROGRAM_NOT_FOUND, programService } from '@/services/programService'
import { getOrderedCommands } from '@/services/workflowService'

export const COMMAND_NOT_FOUND = 'Command does not exist'

async function findCommand(id: number): Promise<ICommand> {
  const [command] = await database
    .select()
    .from(commands)
    .where(eq(commands.id, id))
  if (!command) throw new AppError(COMMAND_NOT_FOUND, 404)
  return command
}

function haveSameIds(first: number[], second: number[]): boolean {
  if (first.length !== second.length) return false
  const sortedSecond = [...second].sort((a, b) => a - b)
  return [...first]
    .sort((a, b) => a - b)
    .every((id, index) => id === sortedSecond[index])
}

export const commandService = {
  async findOwner(id: number): Promise<IEntityOwner | undefined> {
    const [command] = await database
      .select({ ownerEmail: commands.ownerEmail })
      .from(commands)
      .where(eq(commands.id, id))
    return command
  },

  async show(id: number): Promise<ICommand> {
    return findCommand(id)
  },

  // *** New commands are active and go to the end of the workflow order
  async create(
    ownerEmail: string | null,
    workflowId: number,
    data: { name: string; parameters: string; program_id: number }
  ): Promise<ICommand> {
    if (!(await programService.findById(data.program_id))) {
      throw new AppError(PROGRAM_NOT_FOUND, 404)
    }

    return database.transaction(async transaction => {
      const [workflow] = await transaction
        .select({ id: workflows.id })
        .from(workflows)
        .where(eq(workflows.id, workflowId))
      if (!workflow) throw new AppError('Workflow does not exist', 409)

      const [command] = await transaction
        .insert(commands)
        .values({
          name: data.name,
          parameters: data.parameters,
          workflowId,
          ownerEmail,
          programId: data.program_id,
          isActive: true
        })
        .returning()

      const [orderedList] = await transaction
        .select()
        .from(orderedCommandsLists)
        .where(eq(orderedCommandsLists.workflowId, workflowId))
        .for('update')
      if (!orderedList) {
        throw new AppError('OrderedComandsList does not exist')
      }
      await transaction
        .update(orderedCommandsLists)
        .set({ commandIds: [...(orderedList.commandIds ?? []), command.id] })
        .where(eq(orderedCommandsLists.id, orderedList.id))

      return command
    })
  },

  async updateParameters(id: number, parameters: string): Promise<ICommand> {
    const [command] = await database
      .update(commands)
      .set({ parameters })
      .where(eq(commands.id, id))
      .returning()
    if (!command) throw new AppError(COMMAND_NOT_FOUND, 404)
    return command
  },

  async toggleIsActive(id: number): Promise<ICommand> {
    const command = await findCommand(id)
    const [updated] = await database
      .update(commands)
      .set({ isActive: !command.isActive })
      .where(eq(commands.id, id))
      .returning()
    return updated
  },

  // *** The new order must hold exactly the workflow command ids
  async updateOrder(
    workflowId: number,
    newOrder: number[]
  ): Promise<ICommand[]> {
    return database.transaction(async transaction => {
      const [orderedList] = await transaction
        .select()
        .from(orderedCommandsLists)
        .where(eq(orderedCommandsLists.workflowId, workflowId))
        .for('update')
      if (!orderedList) {
        throw new AppError('OrderedComandsList does not exist')
      }
      if (!haveSameIds(orderedList.commandIds ?? [], newOrder)) {
        throw new AppError(
          'newOrder must hold exactly the workflow command ids'
        )
      }

      await transaction
        .update(orderedCommandsLists)
        .set({ commandIds: newOrder })
        .where(eq(orderedCommandsLists.id, orderedList.id))
      return getOrderedCommands(transaction, workflowId)
    })
  },

  // *** The command also leaves the workflow order
  async delete(id: number): Promise<ICommand> {
    return database.transaction(async transaction => {
      const [command] = await transaction
        .delete(commands)
        .where(eq(commands.id, id))
        .returning()
      if (!command) throw new AppError(COMMAND_NOT_FOUND, 404)

      if (command.workflowId !== null) {
        const [orderedList] = await transaction
          .select()
          .from(orderedCommandsLists)
          .where(eq(orderedCommandsLists.workflowId, command.workflowId))
          .for('update')
        if (orderedList) {
          await transaction
            .update(orderedCommandsLists)
            .set({
              commandIds: (orderedList.commandIds ?? []).filter(
                commandId => commandId !== id
              )
            })
            .where(eq(orderedCommandsLists.id, orderedList.id))
        }
      }
      return command
    })
  }
}
