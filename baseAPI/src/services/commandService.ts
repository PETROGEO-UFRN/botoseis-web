import { eq } from 'drizzle-orm'

import database from '@/database/connection'
import { AppError } from '@/errors/AppError'
import { commands, type ICommand } from '@/models/index'
import type { IEntityOwner } from '@/presentation/middlewares/requireAuthentication'
import { orderedCommandsListService } from '@/services/orderedCommandsListService'
import { PROGRAM_NOT_FOUND, programService } from '@/services/programService'

export const COMMAND_NOT_FOUND = 'Command does not exist'

async function findCommand(commandId: number): Promise<ICommand> {
  const [command] = await database
    .select()
    .from(commands)
    .where(eq(commands.id, commandId))
  if (!command) throw new AppError(COMMAND_NOT_FOUND, 404)
  return command
}

export const commandService = {
  async findOwner(commandId: number): Promise<IEntityOwner | undefined> {
    const [commandOwner] = await database
      .select({ ownerEmail: commands.ownerEmail })
      .from(commands)
      .where(eq(commands.id, commandId))
    return commandOwner
  },

  async show(commandId: number): Promise<ICommand> {
    return findCommand(commandId)
  },

  // *** New commands are active and go to the end of the workflow order
  async create(
    ownerEmail: string | null,
    workflowId: number,
    commandData: { name: string; parameters: string; program_id: number }
  ): Promise<ICommand> {
    if (!(await programService.findById(commandData.program_id))) {
      throw new AppError(PROGRAM_NOT_FOUND, 404)
    }

    return database.transaction(async transaction => {
      const [command] = await transaction
        .insert(commands)
        .values({
          name: commandData.name,
          parameters: commandData.parameters,
          workflowId,
          ownerEmail,
          programId: commandData.program_id,
          isActive: true
        })
        .returning()

      await orderedCommandsListService.append(
        transaction,
        workflowId,
        command.id
      )
      return command
    })
  },

  async updateParameters(
    commandId: number,
    parameters: string
  ): Promise<ICommand> {
    const [command] = await database
      .update(commands)
      .set({ parameters })
      .where(eq(commands.id, commandId))
      .returning()
    if (!command) throw new AppError(COMMAND_NOT_FOUND, 404)
    return command
  },

  async toggleIsActive(commandId: number): Promise<ICommand> {
    const command = await findCommand(commandId)
    const [toggledCommand] = await database
      .update(commands)
      .set({ isActive: !command.isActive })
      .where(eq(commands.id, commandId))
      .returning()
    return toggledCommand
  },

  async updateOrder(
    workflowId: number,
    requestedCommandIds: number[]
  ): Promise<ICommand[]> {
    return database.transaction(async transaction => {
      await orderedCommandsListService.replace(
        transaction,
        workflowId,
        requestedCommandIds
      )
      return orderedCommandsListService.listCommands(transaction, workflowId)
    })
  },

  // *** The command also leaves the workflow order
  async delete(commandId: number): Promise<ICommand> {
    return database.transaction(async transaction => {
      const [command] = await transaction
        .delete(commands)
        .where(eq(commands.id, commandId))
        .returning()
      if (!command) throw new AppError(COMMAND_NOT_FOUND, 404)

      if (command.workflowId !== null) {
        await orderedCommandsListService.remove(
          transaction,
          command.workflowId,
          commandId
        )
      }
      return command
    })
  }
}
