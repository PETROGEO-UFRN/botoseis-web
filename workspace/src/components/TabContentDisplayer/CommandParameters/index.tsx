import { useEffect, useState } from "react"
import type { FormEvent } from "react"
import { useShallow } from "zustand/react/shallow"

import { getParameters } from "services/programServices"
import { useSelectedWorkflowsStore } from "store/selectedWorkflowsStore"
import { useCommandsStore } from "store/commandsStore"

import {
  Container,
  CustomButton,
  CustomTooltip
} from "./styles"
import ParameterReadOnly from "./ParameterReadOnly"
import ParameterInput from "./ParameterInput"

interface ICommandParametersProps {
  command: ICommand | undefined
}

export default function CommandParameters({ command }: ICommandParametersProps) {
  const hasSelectedDataset = useSelectedWorkflowsStore(useShallow((state) => (
    state.hasSelectedDataset
  )))
  const updateCommandParams = useCommandsStore(useShallow(state => (
    state.updateCommandParams
  )))

  const [availableParameters, setAvailableParameters] = useState<Array<IParameter>>([])
  const [commandParameters, setCommandParameters] = useState<IobjectWithDynamicFields | null>(null)

  const submitParametersUpdate = (event: FormEvent) => {
    event.preventDefault()
    if (!command || typeof command.id == 'string')
      return
    updateCommandParams(command.id, JSON.stringify(commandParameters))
  }

  useEffect(() => {
    if (!command)
      return
    getParameters(command.program_id).then(result => {
      setAvailableParameters(result)
    })
    setCommandParameters(JSON.parse(command.parameters))
  }, [command])

  return (
    <Container
      onSubmit={submitParametersUpdate}
      $hasGap={!hasSelectedDataset}
    >
      {availableParameters.map((parameterField) => (
        <CustomTooltip
          key={parameterField.id}
          title={parameterField.description}
        >
          {hasSelectedDataset ? (
            <ParameterReadOnly
              name={parameterField.name}
              value={commandParameters ? commandParameters[parameterField.name] : ""}
            />
          ) : (
            <ParameterInput
              parameterField={parameterField}
              commandParameters={commandParameters}
              setCommandParameters={setCommandParameters}
            />
          )}
        </CustomTooltip>
      ))}

      {!hasSelectedDataset && (
        <CustomButton
          type="submit"
          variant="contained"
        >
          Save Parameters
        </CustomButton>
      )}
    </Container>
  )
}
