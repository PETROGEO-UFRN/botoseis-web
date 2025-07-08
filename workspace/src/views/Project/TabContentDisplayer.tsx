import { useCommandsStore } from 'store/commandsStore'
import { useShallow } from 'zustand/react/shallow'

import CommandParameters from 'components/CommandParameters';
import InputSelectorOptions from 'components/InputSelectorOptions';
import OutputConfigOptions from 'components/OutputConfigOptions'
import VizualizerConfigOptions from 'components/VizualizerConfigOptions'

import { StaticTabKey } from 'constants/StaticTabKey'

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