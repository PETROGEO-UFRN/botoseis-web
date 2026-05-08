import styled, { css } from "styled-components";


// ! This styles have some workarrounds remaning on orientation to do stuff
// ! specifically for that given disposal of the related components.
// ! Considerable work would be necessary to make it generic

export function getContainerDirection($orientation: navigationOrientationType) {
  if ($orientation == "horizontal")
    return "column"
  if ($orientation == "vertical")
    return "row"
}

export function getContentOrientationStyles($orientation: navigationOrientationType) {
  if ($orientation == "horizontal")
    return css`
      width: 100%;
      border-radius: 8px 0 0 0;
      height: calc(100% - 48px);
    `
  if ($orientation == "vertical")
    return css`width: calc( 100% - 256px );`
}

export function getContentColorStyles($color: navigationColorType) {
  if ($color !== "white")
    return css`
      border-radius: 0;
      border-left: 2px solid ${({ theme }) => theme.palette.primary.main};
    `
  return css`
    background-color: ${({ theme }) => theme.palette.background.default};
    box-shadow: 0 -8px 16px 4px #0000003F;
  `
}

const getContainerHeight = ($orientation: navigationOrientationType) => {
  if ($orientation == "vertical")
    return css`height: calc(100%);`
  return
}

export const Container = styled.div<IContainerProps>`
  display: flex;
  flex-direction: ${({ $orientation }) => getContainerDirection($orientation)};
  width: 100%;
  .MuiTabs-indicator {
    display: none;
  }
  ${({ $orientation }) => getContainerHeight($orientation)}
`

export const TabContent = styled.div<ITabContentProps>`
  z-index: 2;
  height: 100%;
  width: 100%;
  padding: 8px 16px;
  ${({ $orientation }) => getContentOrientationStyles($orientation)}
  ${({ $color }) => getContentColorStyles($color)}
`
