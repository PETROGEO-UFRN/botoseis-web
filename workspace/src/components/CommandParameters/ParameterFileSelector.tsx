import { useMemo } from "react"
import { useLocation } from "@tanstack/react-location"
import { useShallow } from 'zustand/react/shallow'
import { FileSelector } from "shared-ui"

import { useTablesStore } from 'store/tablesStore'
import { fileDataTypes } from "constants/fileDataTypes"

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
  const location = useLocation()
  const projectId = Number(location.current.pathname.split('/')[2])
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
    newFile: File,
    formData: FormData
  ) => {
    if (fileInputDataType == fileDataTypes.Table)
      uploadNewTableFile(
        formData,
        projectId
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
