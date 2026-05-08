import { Box } from '@mui/material'
import { createFileRoute } from '@tanstack/react-router'

import BokehPlot from '@/components/BokehPlot'
import { PLOT_TYPES_ENUM } from '@/constants/PLOT_TYPES'

export const Route = createFileRoute('/plot/velocity-model/$workflowId')({
  component: VelocityModelPage
})

function VelocityModelPage() {
  const { workflowId } = Route.useParams()

  return (
    <Box sx={{ height: '100vh' }} id="velocity-model-page">
      <BokehPlot
        plotType={PLOT_TYPES_ENUM.VELOCITY_MODEL}
        workflowId={workflowId}
      />
    </Box>
  )
}
