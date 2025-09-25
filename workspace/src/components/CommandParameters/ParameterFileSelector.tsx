import { useState, useEffect, useMemo } from "react"
import { useLocation } from "@tanstack/react-location"
import { useShallow } from 'zustand/react/shallow'
import { FileSelector } from "shared-ui"

import { listHelperFiles, createHelperFile } from "services/helperFileServices"
import { useCommandsStore } from 'store/commandsStore'
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore'

interface IParameterFileSelector {
  label: string
  input_type: IseismicProgramParameters["input_type"]
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
    selectedCommandId,
  } = useCommandsStore(useShallow((state) => ({
    selectedCommandId: state.selectedCommandId,
  })))
  const {
    singleSelectedWorkflowId,
  } = useSelectedWorkflowsStore(useShallow((state) => ({
    singleSelectedWorkflowId: state.singleSelectedWorkflowId,
  })))
  const [fileLinks, setFileLinks] = useState<Array<IfileLink>>([])

  const fileInputDataType: helperFileTypes | undefined = useMemo(() => {
    const [_, dataType] = input_type.split(":")
    if (dataType === "model" || dataType === "table")
      return dataType
    return
  }, [input_type])

  useEffect(() => {
    if (!fileInputDataType)
      return
    listHelperFiles(
      projectId,
      fileInputDataType
    ).then((result) => {
      if (!result)
        return
      setFileLinks(result)
    })
  }, [selectedCommandId])

  const submitGenericHelperFileLinkUpdate = () => { }

  const uploadNewFile = (
    newFile: File,
    formData: FormData
  ) => {
    console.log({ singleSelectedWorkflowId })
    console.log({ fileInputDataType })
    if (!singleSelectedWorkflowId || !fileInputDataType)
      return
    createHelperFile(
      projectId,
      formData,
      fileInputDataType
    ).then((result) => {
      if (!result) return
      setFileLinks([...fileLinks, result.fileLink])
      setSelectedFileLinkId(result.fileLink.id)
    })
  }

  return (
    <FileSelector
      fileLinks={fileLinks}
      selectedFileLinkId={Number(selectedFileLinkId)}
      onSubmitFileLinkUpdate={submitGenericHelperFileLinkUpdate}
      uploadNewFile={uploadNewFile}
      size="small"
      label={label}
    />
  )
}
