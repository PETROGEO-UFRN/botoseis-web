import { AxiosError } from "axios"
import useNotificationStore from 'store/notificationStore';

import api from "./api"

const notificationStore = useNotificationStore.getState()

interface sessionRequestBody {
  email: string
  password: string
}

export async function validateSession(): Promise<boolean> {
  try {
    const response = await api.get(`/session/validate`)
    if (response.status == 204)
      return true
    return false
  } catch (error) {
    console.error(error)
    const axiosError = error as AxiosError
    notificationStore.triggerNotification({
      content: axiosError
    });
    return false
  }
}

export async function createNewSession({
  email,
  password
}: sessionRequestBody): Promise<true | null> {
  try {
    await api.post(`/session/`, {
      email,
      password
    })
    return true
  } catch (error) {
    const axiosError = error as AxiosError
    notificationStore.triggerNotification({
      content: axiosError
    });
    return null
  }
}
