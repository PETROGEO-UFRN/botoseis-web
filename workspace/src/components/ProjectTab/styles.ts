import styled from "styled-components";
import ButtonGroup from '@mui/material/ButtonGroup';

export const Container = styled.div`
  width: 320px;
  height: 100%;
  overflow: auto;
`

export const CustomButtonGroup = styled(ButtonGroup)`
  & button {
    border-radius: 0 0 4px;
  }
  margin-bottom: 16px;
`
