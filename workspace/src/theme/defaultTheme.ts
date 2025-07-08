import { createTheme } from "@mui/material/styles";

const defaultTheme = createTheme({
  palette: {
    primary: {
      main: "#596F69",
      contrastText: "#fff",
    },
    secondary: {
      main: "#725B5B",
      contrastText: "#fff",
    },
    background: {
      default: "#fff",
      paper: "#fff",
    },
    text: {
      primary: "#000",
      secondary: "#000",
    }
  },
});

export default defaultTheme
