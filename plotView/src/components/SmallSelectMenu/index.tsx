import MenuItem from '@mui/material/MenuItem'
import TextField from '@mui/material/TextField'
import type { ChangeEvent } from 'react'

interface ISmallSelectProps {
  label: string
  value: number | string | null
  options: Array<{ id: number | string; label: string }>
  onChange: (event: ChangeEvent<HTMLInputElement>) => void
  fullWidth?: boolean
}

export default function SmallSelectMenu({
  label,
  value,
  options,
  onChange,
  fullWidth = true
}: ISmallSelectProps) {
  return (
    <TextField
      select
      size="small"
      label={label}
      value={value}
      onChange={onChange}
      fullWidth={fullWidth}
    >
      {options.map(option => (
        <MenuItem key={option.id} value={option.id}>
          {option.label}
        </MenuItem>
      ))}
    </TextField>
  )
}
