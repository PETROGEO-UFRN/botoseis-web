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
        Gather Key
      </Typography>

      <TextField
        type='text'
        value={gatherKey}
        onChange={(event) => updateGatherKey(singleSelectedWorkflowId, event.target.value)}
      />
      <HelperText>
        Gather key is mandatory for pre-stack data.
      </HelperText>
      <HelperText>
        Must be provided the key of sorted data.
      </HelperText>
    </Container>
  )
}
