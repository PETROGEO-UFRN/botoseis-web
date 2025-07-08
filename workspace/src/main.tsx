import React from 'react'
import ReactDOM from 'react-dom/client'
import { Routes } from 'generouted/react-location'
import { ThemeProvider as MuiThemeProvider } from '@mui/material'
import { ThemeProvider } from 'styled-components'

import defaultTheme from 'theme/defaultTheme'
import './index.css'

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <MuiThemeProvider theme={defaultTheme}>
    <ThemeProvider theme={defaultTheme}>
      <React.StrictMode>
        <Routes />
      </React.StrictMode >
    </ThemeProvider>
  </MuiThemeProvider>
)
