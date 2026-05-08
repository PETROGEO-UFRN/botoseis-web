import styled, { css } from 'styled-components'
import Button from '@mui/material/Button'

import { IFloatButtonProps } from '../../types/buttonTypes'

export const CustomButton = styled(Button) <IFloatButtonProps>`
  && {
    position: absolute;
    z-index: 10;
    border-radius: 16px;
  }

  ${({ $top }) => $top && css`top: ${$top};`}
  ${({ $bottom }) => $bottom && css`bottom: ${$bottom};`}
  ${({ $left }) => $left && css`left: ${$left};`}
  ${({ $right }) => $right && css`right: ${$right};`}
`
