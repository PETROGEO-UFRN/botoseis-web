import { useEffect, useState } from 'react'
import { useShallow } from 'zustand/react/shallow'

import TextField from "@mui/material/TextField"
import Typography from '@mui/material/Typography'

import { useGatherKeyStore } from 'store/gatherKeyStore'
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore'
import { Container, HelperText } from './styles'

export default function VizualizerConfigOptions() {
  const singleSelectedWorkflowId = useSelectedWorkflowsStore(useShallow(state => state.singleSelectedWorkflowId))
  const [gatherKeys, updateGatherKey] = useGatherKeyStore(useShallow((state) => ([state.gatherKeys, state.updateGatherKey])))
  const [gatherKey, setGatherKey] = useState("")

  useEffect(() => {
    if (!singleSelectedWorkflowId)
      return setGatherKey("")
    const gatherKeyFromStore = gatherKeys.get(singleSelectedWorkflowId)
    if (!gatherKeyFromStore)
      return setGatherKey("")
    setGatherKey(gatherKeyFromStore)
  }, [gatherKeys, singleSelectedWorkflowId])

  return (
    <Container>
      <Typography variant="h5">
        Informe o Gather key
      </Typography>

      <TextField
        type='text'
        value={gatherKey}
        onChange={(event) => updateGatherKey(singleSelectedWorkflowId, event.target.value)}
      />
      <HelperText>
        Gather key is not always mandatory and shall be empty in some cases, depending on your seismic data organization
      </HelperText>
      <HelperText>
        Gather key is only requested when your seismic data file is dived in shot gathers
      </HelperText>
    </Container>
  )
}
