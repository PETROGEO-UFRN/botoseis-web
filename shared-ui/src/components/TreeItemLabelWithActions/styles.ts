import styled, { css } from "styled-components";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";

interface ICustomTextFieldProps {
  $isLoadingUpdate: boolean
}

export const Container = styled(Box)`
  && {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
`

export const CustomTextField = styled(TextField) <ICustomTextFieldProps>`
  && input {
    padding: 2px 8px;
    font-size: 16px;
  }
  && :not(input:focus) + fieldset {
    border: none;
  }
  pointer-events: none;
  width: calc(100% - 72px ${({ $isLoadingUpdate }) => $isLoadingUpdate && " - 24px"} );
`

export const ActionsBox = styled(Box)`
  display: flex;
  gap: 4px;
`
