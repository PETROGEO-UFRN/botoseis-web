import styled, { css } from "styled-components";
import Tab from '@mui/material/Tab';
import IconButton from "@mui/material/IconButton";

export function getCustumTabOrientationStyles($orientation: navigationOrientationType) {
  if ($orientation == "horizontal")
    return css`
      border-radius: 8px 8px 0 0;
      margin-left: 2px;
      :not(.Mui-selected){
        margin-top: 8px;
      }
    `
  if ($orientation == "vertical")
    return css`
      width: 256px;
      border-radius: 8px 0 0 8px;
      margin-bottom: 8px;
    `
}

export function getCustomTabColorStyles($color: navigationColorType) {
  if ($color == "white")
    return css`
      background-color: ${({ theme }) => theme.palette.grey[50]};
      color: ${({ theme }) => theme.palette.primary.main};
      ::after {
        background: linear-gradient(
          to left,
          ${({ theme }) => theme.palette.grey[50]} 32%,
          #0000 100%
        );
      }
      &.Mui-selected {
        background-color: ${({ theme }) => theme.palette.grey[50]};
      }
    `
  return css`
    background-color: ${({ theme }) => theme.palette[$color].light};
    ::after {
      background: linear-gradient(
        to left,
        ${({ theme }) => theme.palette[$color].light} 32%,
        #0000 100%,
      );
    }
    &.Mui-selected {
      color: ${({ theme }) => theme.palette[$color].contrastText};
      background-color: ${({ theme }) => theme.palette[$color].main};
      ::after {
        background: linear-gradient(
          to left,
          ${({ theme }) => theme.palette[$color].main} 32%,
          #0000 100%,
        );
      }
    }
  `
}

export const Container = styled.div`
  position: relative;
`

export const TabBody = styled(Tab) <ICustomTabContainerProps>`
  &.MuiTab-root.MuiButtonBase-root {
    display: flex;
    align-items: flex-start;
    overflow: hidden;
    white-space: nowrap;
    max-width: 256px;

    ${({ $orientation }) => getCustumTabOrientationStyles($orientation)}
    ${({ $color }) => getCustomTabColorStyles($color)}
    ${({ $isActive }) => !$isActive && 'font-style: italic; text-decoration-line: line-through; opacity: 87%'}


    .MuiTouchRipple-root {
      z-index: 3;
    }

    ::after {
      content: '';
      position: absolute;
      right: 0;
      width: 32px;
    }

    :not(.Mui-selected){
      opacity: 86%;
      :hover {
        opacity: 100%;
      }
    }

    &.Mui-selected {
      cursor: auto;
      z-index: 10;
      .MuiTouchRipple-root {
        display: none;
      }
    }
  }
`

export const ActionButtonsContainer = styled.div`
  position: absolute;
  right: 8px;
  top: 2px;
  z-index: 10;
`

export const ActionButton = styled(IconButton)`
  &.MuiIconButton-root {
    z-index: 10;
    
    height: 44px;
    width: 44px;
    color: ${({ theme }) => theme.palette.primary.contrastText};
  }
`
