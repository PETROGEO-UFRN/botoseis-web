import { useEffect, useState } from "react"
import { useLocation } from "@tanstack/react-location"
import { useShallow } from 'zustand/react/shallow'

import Button from "@mui/material/Button"
import Typography from '@mui/material/Typography'

import { FileSelector } from "shared-ui"

import { listSUFiles, createSUFile } from "services/suFileServices"
import { updateWorkflowFileLink } from "services/workflowServices"
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore'
import { useGatherKeyStore } from 'store/gatherKeyStore'

import { Container } from "./styles"

export default function InputSelectorOptions() {
  const location = useLocation()
  const projectId = Number(location.current.pathname.split('/')[2])

  const {
    selectedWorkflows,
    singleSelectedWorkflowId,
    hasSelectedDataset,
  } = useSelectedWorkflowsStore(useShallow((state) => ({
    selectedWorkflows: state.selectedWorkflows,
    singleSelectedWorkflowId: state.singleSelectedWorkflowId,
    hasSelectedDataset: state.hasSelectedDataset,
  })))
  const gatherKeys = useGatherKeyStore(useShallow((state) => state.gatherKeys))

  const [fileLinks, setFileLinks] = useState<Array<IfileLink>>([])
  const [selectedFileLinkId, setSelectedFileLinkId] = useState<number | undefined>(0)

  const uploadNewFile = (
    newFile: File,
    formData: FormData
  ) => {
    if (!singleSelectedWorkflowId)
      return

    createSUFile(
      projectId,
      formData
    ).then((result) => {
      if (!result) return
      updateWorkflowFileLink(
        singleSelectedWorkflowId,
        result.fileLink.id
      )
      setFileLinks([...fileLinks, result.fileLink])
      setSelectedFileLinkId(result.fileLink.id)
    })
  }

  const visualizeInputFile = () => {
    if (!singleSelectedWorkflowId) return

    let vizualizerURL = `${import.meta.env.VITE_VISUALIZER_URL}/?`
    const gatherKeyFromStore = gatherKeys.get(singleSelectedWorkflowId)
    if (gatherKeyFromStore)
      vizualizerURL += `gather_key=${gatherKeyFromStore}&`
    window.open(`${vizualizerURL}workflowId=${singleSelectedWorkflowId}&origin=input`, '_blank')
  }

  const submitWorkflowFileLinkUpdate = (fileLinkId: number) => {
    const oldFileLinkId = selectedFileLinkId
    setSelectedFileLinkId(fileLinkId)

    if (!singleSelectedWorkflowId)
      return
    if (!fileLinkId)
      return

    updateWorkflowFileLink(
      singleSelectedWorkflowId,
      Number(fileLinkId)
    ).catch((error) => {
      console.error(error)
      setSelectedFileLinkId(oldFileLinkId)
    })
  }

  useEffect(() => {
    listSUFiles(projectId).then((result) => {
      if (!result)
        return
      setFileLinks(result)

      const availableSUFiles = selectedWorkflows.filter(
        (workflow) => workflow.id == singleSelectedWorkflowId
      )
      const fileLinkId = availableSUFiles[0].input_file_link_id
      setSelectedFileLinkId(fileLinkId)
    })
  }, [])

  return (
    <Container>
      <Typography variant="h5">
        {
          hasSelectedDataset ?
            "Original .su data for this dataset" :
            "Choose a .su file to be processed on this workflow"
        }
      </Typography>

      {hasSelectedDataset ? (
        <Typography fontSize={22}>
          {fileLinks.find((link) => link.id === selectedFileLinkId)?.name}
        </Typography>
      ) : (
        <FileSelector
          fileLinks={fileLinks}
          selectedFileLinkId={selectedFileLinkId}
          onSubmitFileLinkUpdate={submitWorkflowFileLinkUpdate}
          uploadNewFile={uploadNewFile}
        />
      )}

      <Button
        variant="contained"
        color={hasSelectedDataset ? 'secondary' : 'primary'}
        onClick={visualizeInputFile}
      >
        Visualize input
      </Button>
    </Container>
  )
}
