import { Box } from '@mui/material'
import { createFileRoute } from '@tanstack/react-router'

import BokehPlot from '@/components/BokehPlot'
import { PLOT_TYPES_ENUM } from '@/constants/PLOT_TYPES'

export const Route = createFileRoute('/plot/bandwidth/$workflowId')({
  component: BandwidthPage
})

function BandwidthPage() {
  const { workflowId } = Route.useParams()

  return (
    <Box sx={{ height: '100vh' }} id="bandwidth-page">
      <BokehPlot
        plotType={PLOT_TYPES_ENUM.BANDWIDTH}
        workflowId={workflowId}
      />
    </Box>
  )
}
