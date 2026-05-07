import ChevronRight from '@mui/icons-material/ChevronRight'
import { Box, Button } from '@mui/material'
import { createFileRoute } from '@tanstack/react-router'
import { type ChangeEvent, useState } from 'react'

import BokehPlot from '@/components/BokehPlot'
import CustomSwitch from '@/components/CustomSwitch'
import { PlotActionsDrawer } from '@/components/PlotActionsDrawer'
import { PlotFloatActions } from '@/components/PlotFloatActions'
import SmallSelectMenu from '@/components/SmallSelectMenu'
import {
  AUTOMATIC_GAIN_TYPE_OPTIONS,
  COLORMAP_OPTIONS,
  GAIN_OPTIONS
} from '@/constants/BOKEH_REACT_BRIDGE'
import { PLOT_TYPES_ENUM } from '@/constants/PLOT_TYPES'
import { useBokeh } from '@/hooks/useBokehConnection'

export const Route = createFileRoute('/plot/basic-plot/$workflowId')({
  component: BasicPlotPage
})

const RANGE: Record<
  keyof IGainInputs,
  { min: number; max: number; step: number }
> = {
  AUTOMATIC_GAIN: { min: 0, max: 5, step: 0.01 },
  PERCENTILE_CLIPPING: { min: 1, max: 100, step: 1 }
}

function BasicPlotPage() {
  const { workflowId } = Route.useParams()
  const { emitDebouncedTrigger } = useBokeh()
  const [isDrawerOpen, setIsDrawerOpen] = useState(false)
  const [imageVisible, setImageVisible] = useState(true)
  const [wiggleVisible, setWiggleVisible] = useState(false)
  const [colormap, setColormap] = useState<ColormapType>('grey')
  const [gainType, setGainType] = useState<
    keyof IAutomaticGainOptions | 'None'
  >('None')
  const [gainInputs, setGainInputs] = useState<IGainInputs>({
    AUTOMATIC_GAIN: 0.5,
    PERCENTILE_CLIPPING: 100
  })

  const handleApplyGain = () => {
    emitDebouncedTrigger({
      gain: {
        AGC: gainType === 'AGC' ? gainInputs.AUTOMATIC_GAIN : null,
        GAUSSIAN_AGC:
          gainType === 'GAUSSIAN_AGC' ? gainInputs.AUTOMATIC_GAIN : null,
        PERCENTILE_CLIPPING: gainInputs.PERCENTILE_CLIPPING
      }
    })
  }

  return (
    <Box sx={{ height: '100vh' }} id="basic-plot-page">
      <PlotFloatActions.Root>
        <Button
          size="small"
          variant="outlined"
          onClick={() => setIsDrawerOpen(true)}
        >
          <ChevronRight fontSize="small" /> Options
        </Button>
      </PlotFloatActions.Root>

      <BokehPlot
        plotType={PLOT_TYPES_ENUM.BASIC_PLOT}
        workflowId={workflowId}
      />

      <PlotActionsDrawer.Root isOpen={isDrawerOpen} setIsOpen={setIsDrawerOpen}>
        <PlotActionsDrawer.Group title="Renderers">
          <CustomSwitch
            label="Image"
            isChecked={imageVisible}
            onChange={(_, checked) => {
              setImageVisible(checked)
              emitDebouncedTrigger({ imageVisible: checked })
            }}
          />
          <CustomSwitch
            label="Wiggle"
            isChecked={wiggleVisible}
            onChange={(_, checked) => {
              setWiggleVisible(checked)
              emitDebouncedTrigger({ wiggleVisible: checked })
            }}
          />
        </PlotActionsDrawer.Group>

        <PlotActionsDrawer.Group title="Colormap">
          <SmallSelectMenu
            label="Image colormap"
            value={colormap}
            options={COLORMAP_OPTIONS}
            onChange={(event: ChangeEvent<HTMLInputElement>) => {
              const next = event.target.value as ColormapType
              setColormap(next)
              emitDebouncedTrigger({ colormap: next })
            }}
          />
        </PlotActionsDrawer.Group>

        <PlotActionsDrawer.Group title="Gain" largePadding>
          <SmallSelectMenu
            label="Automatic gain type"
            value={gainType}
            options={AUTOMATIC_GAIN_TYPE_OPTIONS}
            onChange={(event: ChangeEvent<HTMLInputElement>) =>
              setGainType(
                event.target.value as keyof IAutomaticGainOptions | 'None'
              )
            }
          />
          {GAIN_OPTIONS.map(opt => (
            <PlotActionsDrawer.NumberInput
              key={opt.key}
              type="number"
              label={opt.label}
              value={gainInputs[opt.key]}
              onChange={event =>
                setGainInputs(prev => ({
                  ...prev,
                  [opt.key]: Number(event.target.value)
                }))
              }
              {...RANGE[opt.key]}
            />
          ))}
          <Button variant="outlined" onClick={handleApplyGain}>
            Apply gain
          </Button>
        </PlotActionsDrawer.Group>
      </PlotActionsDrawer.Root>
    </Box>
  )
}
