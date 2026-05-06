import TextField from '@mui/material/TextField'
import type { ChangeEvent } from 'react'

interface ILineInputProps {
  value: string | number | null
  label?: string
  type?: 'text' | 'number'
  step?: number
  min?: number
  max?: number
  isLoading?: boolean
  onChange: (event: ChangeEvent<HTMLInputElement>) => void
}

export function NumberInput({
  label,
  value,
  type = 'text',
  step = 1,
  min = -Infinity,
  max = Infinity,
  isLoading = false,
  onChange
}: ILineInputProps) {
  return (
    <TextField
      fullWidth
      size="small"
      type={type}
      label={label}
      value={value}
      disabled={isLoading}
      onChange={onChange}
      slotProps={{
        htmlInput: {
          step: step,
          min: min,
          max: max
        }
      }}
    />
  )
}
