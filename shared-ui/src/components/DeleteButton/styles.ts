import styled from 'styled-components'

import IconButton from '@mui/material/IconButton'
import Button from '@mui/material/Button'
import type { IconButtonProps } from '@mui/material/IconButton';

interface ICustomButtonProps {
  $isHidden: boolean
}

interface ICustomIconButtonProps {
  $isHoverDisable: boolean
}

export const CustomIconButton = styled(IconButton)
  .attrs<Partial<IconButtonProps>>(() => ({
    component: "span"
  })) <ICustomIconButtonProps>`
    && {
      z-index: 1000;
      cursor: ${({ $isHoverDisable }) => $isHoverDisable ? "inherit" : "pointer"};
    }
  `

export const CustomButton = styled(Button) <ICustomButtonProps>`
  && {
    position: absolute;
    right: 0;
    display: ${({ $isHidden }) => !$isHidden ? "flex" : "none"};
  }
`
