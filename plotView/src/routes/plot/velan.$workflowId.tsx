import ChevronRight from '@mui/icons-material/ChevronRight'
import { Box, Button } from '@mui/material'
import { createFileRoute } from '@tanstack/react-router'
import { type ChangeEvent, useMemo, useState } from 'react'

import BokehPlot from '@/components/BokehPlot'
import CustomSwitch from '@/components/CustomSwitch'
import { PlotActionsDrawer } from '@/components/PlotActionsDrawer'
import { PlotFloatActions } from '@/components/PlotFloatActions'
import SmallSelectMenu from '@/components/SmallSelectMenu'
import {
  AUTOMATIC_GAIN_TYPE_OPTIONS,
  GAIN_OPTIONS
} from '@/constants/BOKEH_REACT_BRIDGE'
import { PLOT_TYPES_ENUM } from '@/constants/PLOT_TYPES'
import { useBokeh } from '@/hooks/useBokehConnection'

interface IVelanSearch {
  firstCdp: number | undefined
  lastCdp: number | undefined
  numberOfGathersPerTime: number | undefined
  firstVelocityValue: number | undefined
  lastVelocityValue: number | undefined
  velocityStepSize: number | undefined
}

export const Route = createFileRoute('/plot/velan/$workflowId')({
  component: VelanPage,
  validateSearch: (search: Record<string, unknown>): IVelanSearch => {
    const toNumberOrUndefined = (value: unknown): number | undefined => {
      if (value === undefined || value === null || value === '')
        return undefined
      const n = Number(value)
      return Number.isFinite(n) ? n : undefined
    }

    return {
      firstCdp: toNumberOrUndefined(search.firstCdp),
      lastCdp: toNumberOrUndefined(search.lastCdp),
      numberOfGathersPerTime: toNumberOrUndefined(
        search.numberOfGathersPerTime
      ),
      firstVelocityValue: toNumberOrUndefined(search.firstVelocityValue),
      lastVelocityValue: toNumberOrUndefined(search.lastVelocityValue),
      velocityStepSize: toNumberOrUndefined(search.velocityStepSize)
    }
  }
})

const GAIN_RANGE: Record<
  keyof IGainInputs,
  { min: number; max: number; step: number }
> = {
  AUTOMATIC_GAIN: { min: 0, max: 5, step: 0.01 },
  PERCENTILE_CLIPPING: { min: 1, max: 100, step: 1 }
}

const VELAN_DEFAULTS = {
  firstCdp: 100,
  lastCdp: 500,
  numberOfGathersPerTime: 50,
  firstVelocityValue: 1000,
  lastVelocityValue: 4000,
  velocityStepSize: 25
}

function VelanPage() {
  const { workflowId } = Route.useParams()
  const {
    firstCdp,
    lastCdp,
    numberOfGathersPerTime,
    firstVelocityValue,
    lastVelocityValue,
    velocityStepSize
  } = Route.useSearch()
  const { emitDebouncedTrigger } = useBokeh()
  const [isDrawerOpen, setIsDrawerOpen] = useState(false)
  const [gatherIndex, setGatherIndex] = useState<number>(
    firstCdp ?? VELAN_DEFAULTS.firstCdp
  )
  const [gainType, setGainType] = useState<
    keyof IAutomaticGainOptions | 'None'
  >('None')
  const [gainInputs, setGainInputs] = useState<IGainInputs>({
    AUTOMATIC_GAIN: 0.5,
    PERCENTILE_CLIPPING: 100
  })
  const [isNMOApplied, setIsNMOApplied] = useState(false)
  const [isNMOHyperboleOn, setIsNMOHyperboleOn] = useState(true)

  const setupProps = useMemo(
    () => ({
      first_cdp: firstCdp ?? VELAN_DEFAULTS.firstCdp,
      last_cdp: lastCdp ?? VELAN_DEFAULTS.lastCdp,
      number_of_gathers_per_time:
        numberOfGathersPerTime ?? VELAN_DEFAULTS.numberOfGathersPerTime,
      first_velocity_value:
        firstVelocityValue ?? VELAN_DEFAULTS.firstVelocityValue,
      last_velocity_value: lastVelocityValue ?? VELAN_DEFAULTS.lastVelocityValue,
      velocity_step_size: velocityStepSize ?? VELAN_DEFAULTS.velocityStepSize
    }),
    [
      firstCdp,
      lastCdp,
      numberOfGathersPerTime,
      firstVelocityValue,
      lastVelocityValue,
      velocityStepSize
    ]
  )

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

  const handleToggleNMO = () => {
    const next = !isNMOApplied
    setIsNMOApplied(next)
    emitDebouncedTrigger({ applyNMO: next })
  }

  return (
    <Box sx={{ height: '100vh' }} id="velan-page">
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
            firstGather: firstCdp ?? VELAN_DEFAULTS.firstCdp,
            lastGather: lastCdp ?? VELAN_DEFAULTS.lastCdp,
            gathersPerLoad:
              numberOfGathersPerTime ?? VELAN_DEFAULTS.numberOfGathersPerTime
          }}
        />
      </PlotFloatActions.Root>

      <BokehPlot
        plotType={PLOT_TYPES_ENUM.VELAN}
        workflowId={workflowId}
        setupProps={setupProps}
      />

      <PlotActionsDrawer.Root isOpen={isDrawerOpen} setIsOpen={setIsDrawerOpen}>
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
              {...GAIN_RANGE[opt.key]}
            />
          ))}
          <Button variant="outlined" onClick={handleApplyGain}>
            Apply gain
          </Button>
        </PlotActionsDrawer.Group>

        <PlotActionsDrawer.Group title="NMO Tools">
          <Button variant="outlined" onClick={handleToggleNMO}>
            {isNMOApplied ? 'Remove NMO' : 'Apply NMO'}
          </Button>
          <CustomSwitch
            label="NMO hyperbola on hover"
            isChecked={isNMOHyperboleOn}
            onChange={(_, checked) => {
              setIsNMOHyperboleOn(checked)
              emitDebouncedTrigger({ isNMOHyperboleOn: checked })
            }}
          />
        </PlotActionsDrawer.Group>

        <PlotActionsDrawer.Group title="Picks">
          <Button
            variant="outlined"
            onClick={() => emitDebouncedTrigger({ reusePicks: true })}
          >
            Reuse picks (CDP 1 → CDP 2)
          </Button>
          <Button
            variant="outlined"
            onClick={() => emitDebouncedTrigger({ savePicks: true })}
          >
            Save picks
          </Button>
        </PlotActionsDrawer.Group>
      </PlotActionsDrawer.Root>
    </Box>
  )
}
