import { Box } from '@mui/material'
import { createFileRoute } from '@tanstack/react-router'

import BokehPlot from '@/components/BokehPlot'
import { PLOT_TYPES_ENUM } from '@/constants/PLOT_TYPES'

interface IBandwidthSearch {
  origin: OriginType | undefined
}

export const Route = createFileRoute('/plot/bandwidth/$workflowId')({
  component: BandwidthPage,
  validateSearch: (search: Record<string, unknown>): IBandwidthSearch => ({
    origin: search.origin === 'input' ? 'input' : undefined
  })
})

function BandwidthPage() {
  const { workflowId } = Route.useParams()
  const { origin } = Route.useSearch()

  return (
    <Box sx={{ height: '100vh' }} id="bandwidth-page">
      <BokehPlot
        plotType={PLOT_TYPES_ENUM.BANDWIDTH}
        workflowId={workflowId}
        origin={origin}
      />
    </Box>
  )
}
