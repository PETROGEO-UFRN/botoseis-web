import { useCommandsStore } from 'store/commandsStore'
import { useShallow } from 'zustand/react/shallow'

import { StaticTabKey } from 'constants/clientPrograms'

import CommandParameters from './CommandParameters'
import InputSelectorOptions from './InputSelectorOptions'
import OutputConfigOptions from './OutputConfigOptions'
import VizualizerConfigOptions from './VizualizerConfigOptions'

export default function TabContentDisplayer() {
  const {
    commands,
    selectedCommandId,
  } = useCommandsStore(useShallow((state) => ({
    commands: state.commands,
    selectedCommandId: state.selectedCommandId,
  })))

  const getTabContent = () => {
    switch (selectedCommandId) {
      case StaticTabKey.Input:
        return <InputSelectorOptions />

      case StaticTabKey.Output:
        return <OutputConfigOptions />

      case StaticTabKey.Vizualizer:
        return <VizualizerConfigOptions />

      case StaticTabKey.Velan:
        return <VizualizerConfigOptions />

      default:
        const selectedCommand = commands.find(({ id }) => id == selectedCommandId)
        if (typeof selectedCommand?.id != "string")
          return (
            <CommandParameters
              command={selectedCommand}
            />
          )
        return <></>
    }
  }

  return selectedCommandId ? getTabContent() : <></>
}