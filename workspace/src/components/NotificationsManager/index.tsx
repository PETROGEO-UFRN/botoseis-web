import { useEffect } from "react"
import { useShallow } from "zustand/react/shallow"
import { useSnackbar } from 'notistack'
import { useNavigate } from '@tanstack/react-location'
import { AxiosError } from "axios"
import type { ReactNode } from "react"

import useNotificationStore from "store/notificationStore"

import CustomErrorMessage from "components/CustomErrorMessage"

interface INotificationManager {
  children: ReactNode
}

export default function NotificationManager({ children }: INotificationManager) {
  const navigate = useNavigate()
  const { enqueueSnackbar } = useSnackbar();
  const notificationMessage = useNotificationStore(useShallow((state) => state.notificationMessage))

  const handleNotificationDiplay = () => {
    if (!notificationMessage)
      return
    if (notificationMessage.content instanceof AxiosError) {
      if (notificationMessage.content.status == 401) {
        enqueueSnackbar(
          <CustomErrorMessage content="Authentication error, redirecting..." />,
          { variant: "error" }
        );
        return navigate({ to: "/login" })
      }
    }

    if (notificationMessage.content instanceof Error) {
      return enqueueSnackbar(
        <CustomErrorMessage content={notificationMessage.content.message} />,
        { variant: "error" }
      );
    }
    enqueueSnackbar(
      <CustomErrorMessage content={notificationMessage.content} />,
      { variant: notificationMessage.variant }
    );
  }

  useEffect(() => {
    handleNotificationDiplay()
  }, [notificationMessage])

  return (<>{children}</>)
}
