import ChevronRight from '@mui/icons-material/ChevronRight'
import { Box, Button, CircularProgress } from '@mui/material'
import { createFileRoute } from '@tanstack/react-router'
import { useState } from 'react'

import BokehPlot from '@/components/BokehPlot'
import { PlotActionsDrawer } from '@/components/PlotActionsDrawer'
import { PlotFloatActions } from '@/components/PlotFloatActions'
import { PLOT_TYPES_ENUM } from '@/constants/PLOT_TYPES'
import { useBokeh } from '@/hooks/useBokehConnection'

export const Route = createFileRoute('/plot/sample/$workflowId')({
  component: SamplePage
})

function SamplePage() {
  const { workflowId } = Route.useParams()
  const { emitDebouncedTrigger } = useBokeh()
  const [pinging, setPinging] = useState(false)
  const [isDrawerOpen, setIsDrawerOpen] = useState(false)
  const [gatherIndex, setGatherIndex] = useState(0)

  const handlePing = () => {
    setPinging(true)
    emitDebouncedTrigger({ ping: true }).finally(() => setPinging(false))
  }

  return (
    <Box sx={{ height: '100vh' }} id="sample-page">
      <PlotFloatActions.Root>
        <Button
          size="small"
          variant="outlined"
          onClick={() => setIsDrawerOpen(true)}
        >
          <ChevronRight fontSize="small" /> Options
        </Button>
        <PlotFloatActions.GatherNavigation
          gatherIndex={gatherIndex}
          setGatherIndex={setGatherIndex}
          bounds={{
            firstGather: 0,
            lastGather: 100,
            gathersPerLoad: 1
          }}
        />
      </PlotFloatActions.Root>

      <BokehPlot
        plotType={PLOT_TYPES_ENUM.SAMPLE_PLOT}
        workflowId={workflowId}
      />

      <PlotActionsDrawer.Root isOpen={isDrawerOpen} setIsOpen={setIsDrawerOpen}>
        <PlotActionsDrawer.Group title="Smoke test">
          <Button variant="contained" onClick={handlePing} disabled={pinging}>
            {pinging ? <CircularProgress size={18} /> : 'Ping'}
          </Button>
        </PlotActionsDrawer.Group>
      </PlotActionsDrawer.Root>
    </Box>
  )
}
