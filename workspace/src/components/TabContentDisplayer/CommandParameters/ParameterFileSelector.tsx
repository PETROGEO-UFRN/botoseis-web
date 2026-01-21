import { useMemo } from "react"
import { useShallow } from 'zustand/react/shallow'
import { FileSelector } from "shared-ui"

import { useTablesStore } from 'store/tablesStore'
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore'
import { fileDataTypes } from "constants/fileDataTypes"
import { useLinesStore } from "store/linesStore"

interface IParameterFileSelector {
  label: string
  input_type: IParameter["input_type"]
  selectedFileLinkId: string | number | boolean
  setSelectedFileLinkId: (newId: string | number) => void
}

export default function ParameterFileSelector({
  label,
  input_type,
  selectedFileLinkId,
  setSelectedFileLinkId,
}: IParameterFileSelector) {
  const lines = useLinesStore(useShallow((state) => state.lines))
  const singleSelectedWorkflowId = useSelectedWorkflowsStore(
    useShallow((state) => state.singleSelectedWorkflowId)
  )
  const {
    tables,
    uploadNewTableFile,
  } = useTablesStore(useShallow((state) => ({
    tables: state.tables,
    uploadNewTableFile: state.uploadNewTableFile,
  })))

  const fileInputDataType: helperFileTypes | undefined = useMemo(() => {
    const [_, dataType] = input_type.split(":")
    if (dataType === "model" || dataType === "table")
      return dataType
    return
  }, [input_type])

  const files: Array<IfileLink> = useMemo(() => {
    if (fileInputDataType == fileDataTypes.Table)
      return tables
    return []
  }, [
    fileInputDataType,
    // *** this condition triggers updates by changes on "tables"
    // *** only if "table" is in "input_type" 
    fileInputDataType === fileDataTypes.Table ? tables : null
  ])

  const uploadNewFile = (
    _newFile: File,
    formData: FormData
  ) => {
    if (!singleSelectedWorkflowId || fileInputDataType != fileDataTypes.Table)
      return

    const selectedLine = lines.find(
      line => line.workflows.find(
        workflow => workflow.id == singleSelectedWorkflowId
      )
    )
    if (!selectedLine) return

    uploadNewTableFile(
      formData,
      selectedLine.id
    ).then(newFileLinkId => {
      if (!newFileLinkId)
        return
      setSelectedFileLinkId(newFileLinkId)
    })
  }

  return (
    <FileSelector
      fileLinks={files}
      selectedFileLinkId={Number(selectedFileLinkId)}
      onSubmitFileLinkUpdate={setSelectedFileLinkId}
      uploadNewFile={uploadNewFile}
      label={label}
      size="small"
    />
  )
}
