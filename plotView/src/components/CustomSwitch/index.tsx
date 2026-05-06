import FormControlLabel from '@mui/material/FormControlLabel'
import Switch from '@mui/material/Switch'
import type { ChangeEvent } from 'react'

interface ICustomSwitchProps {
  label: string
  isChecked: boolean
  onChange: (event: ChangeEvent<HTMLInputElement>, checked: boolean) => void
}

export default function CustomSwitch({
  label,
  isChecked,
  onChange
}: ICustomSwitchProps) {
  return (
    <FormControlLabel
      label={label}
      control={<Switch size="small" checked={isChecked} onChange={onChange} />}
    />
  )
}
