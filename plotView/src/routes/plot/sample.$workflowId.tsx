import { Box, Button, CircularProgress } from '@mui/material'
import { createFileRoute } from '@tanstack/react-router'
import { useState } from 'react'

import BokehPlot from '@/components/BokehPlot'
import { PLOT_TYPES_ENUM } from '@/constants/PLOT_TYPES'
import { useBokeh } from '@/hooks/useBokehConnection'

export const Route = createFileRoute('/plot/sample/$workflowId')({
  component: SamplePage
})

function SamplePage() {
  const { workflowId } = Route.useParams()
  const { emitDebouncedTrigger } = useBokeh()
  const [pinging, setPinging] = useState(false)

  const handlePing = () => {
    setPinging(true)
    emitDebouncedTrigger({ ping: true }).finally(() => setPinging(false))
  }

  return (
    <Box
      sx={{
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        gap: 2,
        p: 2
      }}
    >
      <Button variant="contained" onClick={handlePing} disabled={pinging}>
        {pinging ? <CircularProgress size={18} /> : 'Ping'}
      </Button>
      <BokehPlot
        plotType={PLOT_TYPES_ENUM.SAMPLE_PLOT}
        workflowId={workflowId}
      />
    </Box>
  )
}
