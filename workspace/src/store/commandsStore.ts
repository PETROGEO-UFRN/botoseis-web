import { create } from 'zustand'

import { updateCommandParameters } from 'services/commandServices'
import { getWorkflowByID } from 'services/workflowServices'
import {
  preProcessingCommands,
  postProcessingCommands,
  StaticTabKey
} from 'constants/staticCommands'
import type { IstaticTab } from 'constants/staticCommands'

// ! StaticTabKey here looks too much, needs refactoring
type selectedCommandIdType = number | StaticTabKey
type commandsType = Array<ICommand | IstaticTab>

interface ICommandsStoreState {
  selectedCommandId: selectedCommandIdType
  setSelectedCommandId: (newIndex: number) => void
  commands: commandsType
  setCommands: (newValue: commandsType) => void
  loadCommands: (workflowId: number) => void
  updateCommandParams: (id: number, newParameters: string) => Promise<void>
}

export const useCommandsStore = create<ICommandsStoreState>((set, get) => ({
  selectedCommandId: StaticTabKey.Input,
  setSelectedCommandId: (newIndex) => {
    set(() => ({ selectedCommandId: newIndex }))
  },
  commands: [],
  setCommands: (newValue) => set(() => {
    return ({ commands: [...newValue] })
  }),
  loadCommands: (workflowId) => {
    getWorkflowByID(workflowId)
      .then((result) => {
        if (!result)
          return

        set({
          commands: [
            ...preProcessingCommands,
            ...result.commands,
            ...postProcessingCommands
          ]
        })
        if (result.commands.length < 1)
          return;
        set({ selectedCommandId: result.commands[0].id })
      })
  },
  updateCommandParams: async (id: number | StaticTabKey, newParameters: string) => {
    const commandIndexToUpdate = get().commands.findIndex(
      (command) => command.id == id
    )

    if (!get().commands[commandIndexToUpdate])
      return;
    const updatedCommand = await updateCommandParameters(id, newParameters)
    if (!updatedCommand)
      return
    set((state) => ({
      commands: [...state.commands.map((command, commandIndex) => {
        if (commandIndex == commandIndexToUpdate)
          if (command)
            command.parameters = updatedCommand.parameters
        return command
      })]
    }))
  },
}))
