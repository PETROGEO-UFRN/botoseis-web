import ChevronLeftIcon from '@mui/icons-material/ChevronLeft'
import ChevronRightIcon from '@mui/icons-material/ChevronRight'
import IconButton from '@mui/material/IconButton'
import type { Dispatch, SetStateAction, SubmitEvent } from 'react'

import { useBokeh } from '@/hooks/useBokehConnection'
import { NavigationTextField } from './styles'

interface IGatherBounds {
  firstGather: number
  /** Last selectable gather index; null = open upper bound (server clamps). */
  lastGather: number | null
  gathersPerLoad: number
}

interface IGatherNavigationProps {
  gatherIndex: number
  setGatherIndex: Dispatch<SetStateAction<number>>
  bounds: IGatherBounds
}

export default function GatherNavigation({
  gatherIndex,
  setGatherIndex,
  bounds
}: IGatherNavigationProps) {
  const { emitDebouncedTrigger } = useBokeh()
  const { firstGather: min, lastGather: max, gathersPerLoad: step } = bounds

  const clampGather = (value: number) => {
    let next = Math.max(min, value)
    if (max !== null) next = Math.min(max, next)
    return next
  }

  // The component owns emission so every consumer behaves the same. Stepping and
  // Enter snap the field to the clamped gather; the server always gets a clamped
  // value. Callers just pass a plain state setter.
  const goToGather = (value: number) => {
    const next = clampGather(value)
    setGatherIndex(next)
    emitDebouncedTrigger({ gatherIndex: next })
  }

  // Typing keeps whatever the user enters in the field (so a value whose prefix
  // is below `min` -- e.g. Velan's min of 100 -- can still be typed), while the
  // emitted gather is clamped. Snapping happens on Enter / step.
  const handleInputChange = (raw: number) => {
    setGatherIndex(raw)
    emitDebouncedTrigger({ gatherIndex: clampGather(raw) })
  }

  const submitGatherChange = (event: SubmitEvent) => {
    event.preventDefault()
    goToGather(gatherIndex)
  }

  return (
    <form onSubmit={submitGatherChange}>
      <NavigationTextField
        size="small"
        type="number"
        label="Gather Index"
        value={gatherIndex}
        onChange={event => handleInputChange(Number(event.target.value))}
        slotProps={{
          htmlInput: { min, max: max ?? undefined, step },
          input: {
            startAdornment: (
              <IconButton
                size="small"
                disabled={gatherIndex <= min}
                onClick={() => goToGather(gatherIndex - step)}
              >
                <ChevronLeftIcon fontSize="small" />
              </IconButton>
            ),
            endAdornment: (
              <IconButton
                size="small"
                disabled={max !== null && gatherIndex >= max}
                onClick={() => goToGather(gatherIndex + step)}
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
