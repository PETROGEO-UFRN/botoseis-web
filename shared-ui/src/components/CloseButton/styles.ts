import styled, { css } from 'styled-components'
import IconButton from '@mui/material/IconButton'

import { IFloatButtonProps } from '../../types/buttonTypes'

export const Container = styled(IconButton) <IFloatButtonProps>`
  && {
    position: absolute !important;
    z-index: 10;
    top: -6px;
    left: 16px;

    ${({ $top }) => $top && css`top: ${$top};`}
    ${({ $bottom }) => $bottom && css`bottom: ${$bottom};`}
    ${({ $left }) => $left && css`left: ${$left};`}
    ${({ $right }) => $right && css`right: ${$right};`}
  }
`
