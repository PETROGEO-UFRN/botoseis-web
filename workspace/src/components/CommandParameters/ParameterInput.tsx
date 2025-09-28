import type { Dispatch, SetStateAction } from "react"

import ParameterFileSelector from "./ParameterFileSelector"
import {
  CustomTextField,
} from "./styles"

interface IParameterTextField {
  commandParameters: IobjectWithDynamicFields | null
  setCommandParameters: Dispatch<SetStateAction<IobjectWithDynamicFields | null>>
  parameterField: IParameter
}

export default function ParameterInput({
  parameterField,
  commandParameters,
  setCommandParameters,
}: IParameterTextField) {
  return parameterField.input_type.includes("file") ? (
    <ParameterFileSelector
      label={`${parameterField.name} - Select file`}
      input_type={parameterField.input_type}
      selectedFileLinkId={commandParameters ? commandParameters[parameterField.name] : ""}
      setSelectedFileLinkId={(newId: string | number) => {
        const temCommandParameters = { ...commandParameters }
        temCommandParameters[parameterField.name] = newId
        setCommandParameters({ ...temCommandParameters })
      }}
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
      size="small"
      slotProps={{
        inputLabel: {
          shrink: true,
        },
      }}
    />
  )
}
