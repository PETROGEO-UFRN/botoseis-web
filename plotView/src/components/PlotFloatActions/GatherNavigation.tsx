import ChevronLeftIcon from '@mui/icons-material/ChevronLeft'
import ChevronRightIcon from '@mui/icons-material/ChevronRight'
import IconButton from '@mui/material/IconButton'
import type { Dispatch, SetStateAction, SubmitEvent } from 'react'

import { useBokeh } from '@/hooks/useBokehConnection'
import { NavigationTextField } from './styles'

interface IGatherNavigationSetupProps {
  first_cdp: number
  last_cdp: number | null
  number_of_gathers_per_time: number
}

interface IGatherNavigationProps {
  gatherIndex: number
  setGatherIndex: Dispatch<SetStateAction<number>>
  setupProps: IGatherNavigationSetupProps
}

export default function GatherNavigation({
  gatherIndex,
  setGatherIndex,
  setupProps
}: IGatherNavigationProps) {
  const { emitDebouncedTrigger } = useBokeh()
  const min = setupProps.first_cdp
  const max = setupProps.last_cdp
  const step = setupProps.number_of_gathers_per_time

  const handleStepButton = (direction: 'next' | 'previous') => {
    if (max === null) return
    const stepValue = direction === 'next' ? step : -step
    const newIndex = gatherIndex + stepValue
    setGatherIndex(newIndex)
    emitDebouncedTrigger({ gatherIndex: newIndex })
  }

  const submitGatherChange = (event: SubmitEvent) => {
    event.preventDefault()
    emitDebouncedTrigger({ gatherIndex: gatherIndex })
  }

  return (
    <form onSubmit={submitGatherChange}>
      <NavigationTextField
        size="small"
        type="number"
        label="Gather Index"
        value={gatherIndex}
        onChange={event => setGatherIndex(Number(event.target.value))}
        slotProps={{
          htmlInput: { min, max, step },
          input: {
            startAdornment: (
              <IconButton
                size="small"
                disabled={gatherIndex <= (min ?? 0)}
                onClick={() => handleStepButton('previous')}
              >
                <ChevronLeftIcon fontSize="small" />
              </IconButton>
            ),
            endAdornment: (
              <IconButton
                size="small"
                disabled={gatherIndex >= (max ?? 0)}
                onClick={() => handleStepButton('next')}
              >
                <ChevronRightIcon fontSize="small" />
              </IconButton>
            )
          }
        }}
      />
    </form>
  )
}
