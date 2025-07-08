import { useEffect, useState } from "react"
import type { FormEvent } from "react"
import { useShallow } from "zustand/react/shallow"

import { getParameters } from "services/programServices"
import { useSelectedWorkflowsStore } from "store/selectedWorkflowsStore"
import { useCommandsStore } from "store/commandsStore"

import {
  Container,
  CustomTextField,
  CustomButton,
  CustomTooltip
} from "./styles"
import ParameterReadOnly from "./ParameterReadOnly"

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

  const [availableParameters, setAvailableParameters] = useState<Array<IseismicProgramParameters>>([])
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
            <CustomTextField
              label={parameterField.name}
              // todo: "type" must be improved to handle complex typing rendering stuff like a select list 
              type={parameterField.input_type}
              // ! display "required" status some other way
              // required={parameterField.isRequired}

              value={commandParameters ? commandParameters[parameterField.name] : ""}
              onChange={(event) => {
                const temCommandParameters = { ...commandParameters }
                temCommandParameters[parameterField.name] = event.target.value
                setCommandParameters({ ...temCommandParameters })
              }}
              slotProps={{
                inputLabel: {
                  shrink: true,
                },
              }}
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
