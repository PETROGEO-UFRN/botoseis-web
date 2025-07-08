import { useEffect, useState } from 'react'
import { useShallow } from 'zustand/react/shallow'
import type { ChangeEvent } from 'react'

import Button from "@mui/material/Button"
import TextField from "@mui/material/TextField"
import Typography from '@mui/material/Typography'

import { updateWorkflowOutputName } from 'services/workflowServices'
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore'
import { Container } from './styles'

export default function OutputConfigOptions() {
  const singleSelectedWorkflowId = useSelectedWorkflowsStore(useShallow((state) => state.singleSelectedWorkflowId))
  const selectedWorkflows = useSelectedWorkflowsStore(useShallow((state) => state.selectedWorkflows))
  const [outputFileName, setOutputFileName] = useState("")

  const updateOutputFileName = (event: ChangeEvent<HTMLInputElement>) => {
    const filteredOutputFileName = event.target.value.replace(/[^a-zA-Z0-9\-_()]/g, '')
    setOutputFileName(filteredOutputFileName)
  }

  const submitOutputName = () => {
    if (!singleSelectedWorkflowId) return
    updateWorkflowOutputName(singleSelectedWorkflowId, outputFileName)
  }

  useEffect(() => {
    selectedWorkflows.forEach((workflow) => {
      if (workflow.id == singleSelectedWorkflowId)
        setOutputFileName(workflow.output_name)
    })
  }, [singleSelectedWorkflowId])

  return (
    <Container>
      <Typography variant="h5">
        Informe o nome do output
      </Typography>
      <TextField
        type='text'
        value={outputFileName}
        onChange={updateOutputFileName}
      />

      <Button
        variant='contained'
        onClick={submitOutputName}
      >
        Salvar novo nome
      </Button>
    </Container>
  )
}
