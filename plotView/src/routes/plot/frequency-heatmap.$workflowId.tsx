import { Box } from '@mui/material'
import { createFileRoute } from '@tanstack/react-router'

import BokehPlot from '@/components/BokehPlot'
import { PLOT_TYPES_ENUM } from '@/constants/PLOT_TYPES'

export const Route = createFileRoute('/plot/frequency-heatmap/$workflowId')({
  component: FrequencyHeatmapPage
})

function FrequencyHeatmapPage() {
  const { workflowId } = Route.useParams()

  return (
    <Box sx={{ height: '100vh' }} id="frequency-heatmap-page">
      <BokehPlot
        plotType={PLOT_TYPES_ENUM.FREQUENCY_HEATMAP}
        workflowId={workflowId}
      />
    </Box>
  )
}
