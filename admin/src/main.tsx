import React from 'react'
import ReactDOM from 'react-dom/client'
import { Routes } from 'generouted/react-location'

import GroupsProvider from './providers/GroupsProvider'
import SelectedProgramProvider from './providers/SelectedProgramProvider'

import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <GroupsProvider>
      <SelectedProgramProvider>
        <Routes />
      </SelectedProgramProvider>
    </GroupsProvider>
  </React.StrictMode>,
)
