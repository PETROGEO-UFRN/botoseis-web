import { Box } from '@mui/material'
import { createFileRoute } from '@tanstack/react-router'

import BokehPlot from '@/components/BokehPlot'
import { PLOT_TYPES_ENUM } from '@/constants/PLOT_TYPES'

export const Route = createFileRoute('/plot/bandwidth/$workflowId')({
  component: BandwidthPage
})

function BandwidthPage() {
  const { workflowId } = Route.useParams()

  // Bandwidth reads no file of its own: it is driven by the cross-tab observer
  // feed (the section BasicPlot is showing for this workflowId), so it needs no
  // origin / gather params.
  return (
    <Box sx={{ height: '100vh' }} id="bandwidth-page">
      <BokehPlot plotType={PLOT_TYPES_ENUM.BANDWIDTH} workflowId={workflowId} />
    </Box>
  )
}
