import { AxiosError } from "axios"
import useNotificationStore from 'store/notificationStore';

import api from "./api"

const notificationStore = useNotificationStore.getState()

interface sessionRequestBody {
  email: string
  password: string
}

export async function validateSession(): Promise<boolean> {
  const token = "mock-token"
  try {
    // ! insecure
    const response = await api.get(`/session/validate/${token}`)
    if (response.status == 200)
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
    console.log("try to login")
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
