import { Alert, CircularProgress } from '@mui/material'
import { useEffect, useRef, useState } from 'react'

import type { PLOT_TYPES_ENUM } from '@/constants/PLOT_TYPES'
import { useBokehLoader } from '@/hooks/useBokehLoader'
import { Container, PlotBox } from './styles'

interface IBokehPlotProps {
  plotType: PLOT_TYPES_ENUM
  workflowId: string
  setupProps?: plotSetupPropsType
}

const CONNECTION_RETRY_TIMEOUT_MS = 5000

/**
 * BokehPlot Component.
 * Acts as bridge between React and the Bokeh Tornado Server.
 * Handles script injection, server restarts (autoreload)
 */
export default function BokehPlot({
  plotType,
  workflowId,
  setupProps
}: IBokehPlotProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const { loadBokehScripts } = useBokehLoader(containerRef)

  const [loading, setLoading] = useState(true)
  const [requestLog, setRequestLog] = useState<string | null>(null)

  useEffect(() => {
    let retryTimeout: NodeJS.Timeout | null = null

    setRequestLog(null)
    setRequestLog('Connecting to Bokeh server...')

    loadBokehScripts({ plotType, workflowId, setupProps }).then(result => {
      if (result.ok) {
        if (retryTimeout) clearTimeout(retryTimeout)
        setRequestLog(null)
        setLoading(false)
        return
      }

      console.warn(
        `Connection failed, retrying in ${CONNECTION_RETRY_TIMEOUT_MS / 1000}s...`
      )
      retryTimeout = setTimeout(
        () => loadBokehScripts({ plotType, workflowId, setupProps }),
        CONNECTION_RETRY_TIMEOUT_MS
      )
    })

    return () => {
      // *** Stop retries and clear refs if the component unmounts
      if (retryTimeout) clearTimeout(retryTimeout)
    }
  }, [loadBokehScripts, plotType, workflowId, setupProps])

  return (
    <Container>
      {loading && !requestLog && <CircularProgress size={24} />}

      {requestLog && (
        <Alert severity="info" sx={{ mb: 2 }}>
          {requestLog}
        </Alert>
      )}

      <PlotBox ref={containerRef} id="bokeh-plot-container" />
    </Container>
  )
}
