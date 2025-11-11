import styled from "styled-components"

import TextField from "@mui/material/TextField"

export const Container = styled.form`
  display: flex;
  flex-direction: column;
  flex-wrap: wrap;

  height: 100%;
  width: 100%;
  padding-top: 8px;
  gap: 16px;
`

export const CustomTextField = styled(TextField)`
  label {
    font-size: 20px;
    transform: translate(14px, -16px) scale(100%);
  }
  legend {
    font-size: 22px;
  }
`