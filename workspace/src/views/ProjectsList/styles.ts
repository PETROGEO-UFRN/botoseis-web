import styled from 'styled-components'

import TableCell from '@mui/material/TableCell';
import Fab from '@mui/material/Fab';

export const Container = styled.div`
  position: relative;

  width: 100vw;
  height: 100vh;
  overflow: auto;
`

export const CustomHeadCell = styled(TableCell)`
  &.MuiTableCell-root {
    background-color: ${({ theme }) => theme.palette.primary.main};
    color: ${({ theme }) => theme.palette.primary.contrastText};
    font-weight: 700;
    font-size: 18px;
    letter-spacing: 2px;
  }
`

export const AddProjectButton = styled(Fab)`
  &.MuiFab-root {
    position: absolute;
    bottom: 32px;
    right: 32px;
  }
`
