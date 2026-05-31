import ChevronLeftIcon from '@mui/icons-material/ChevronLeft'
import Drawer from '@mui/material/Drawer'
import type { Dispatch, ReactNode, SetStateAction } from 'react'

import { CloseIconButton, RootCustomStack } from './styles'

interface IPlotActionsDrawerRootProps {
  isOpen: boolean
  setIsOpen: Dispatch<SetStateAction<boolean>>
  children?: ReactNode
}

export function Root({
  isOpen,
  setIsOpen,
  children
}: IPlotActionsDrawerRootProps) {
  return (
    <Drawer open={isOpen} onClose={() => setIsOpen(false)} anchor="left">
      <CloseIconButton size="small" onClick={() => setIsOpen(false)}>
        <ChevronLeftIcon />
      </CloseIconButton>

      <RootCustomStack direction="column" fullSize>
        {children}
      </RootCustomStack>
    </Drawer>
  )
}
