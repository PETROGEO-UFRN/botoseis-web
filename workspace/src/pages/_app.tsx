import { Outlet } from '@tanstack/react-location'
import { SnackbarProvider } from 'notistack'

import NotificationManager from 'components/NotificationsManager'


export default function App() {
  return (
    <SnackbarProvider maxSnack={10}>
      <NotificationManager>
        <Outlet />
      </NotificationManager>
    </SnackbarProvider>
  )
}