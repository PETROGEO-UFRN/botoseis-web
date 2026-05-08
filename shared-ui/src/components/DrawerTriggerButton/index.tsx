import type { ReactNode, Dispatch, SetStateAction } from 'react';

import type { IFloatButtonProps } from '../../types/buttonTypes'


import {
  CustomButton
} from './styles'


interface IDrawerTriggerButton extends IFloatButtonProps {
  children?: ReactNode
  setIsOpen: Dispatch<SetStateAction<boolean>>
  startIcon?: ReactNode
  endIcon?: ReactNode
}

export default function DrawerTriggerButton({
  children,
  setIsOpen,
  startIcon,
  endIcon,

  $top,
  $bottom,
  $left,
  $right,
}: IDrawerTriggerButton) {
  return (
    <CustomButton
      size='small'
      color='secondary'
      variant='contained'
      onClick={() => setIsOpen(true)}
      startIcon={startIcon}
      endIcon={endIcon}

      $top={$top}
      $bottom={$bottom}
      $left={$left}
      $right={$right}
    >
      {children}
    </CustomButton>
  )
}
