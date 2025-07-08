import { AxiosError } from "axios"
import useNotificationStore from 'store/notificationStore';

import api from "./api"

const notificationStore = useNotificationStore.getState()

export async function getLinesByProjectID(
  projectId: number
): Promise<Array<ILine> | null> {
  try {
    const response = await api.get<Array<ILine>>(`/line/list/${projectId}`)
    return response.data
  } catch (error) {
    console.error(error);
    const axiosError = error as AxiosError
    notificationStore.triggerNotification({
      content: axiosError
    });
    return null
  }
}

export async function createNewLine(
  projectId: number,
  name: string
): Promise<ILine | null> {
  try {
    const response = await api.post<ILine>(
      `/line/create/${projectId}`,
      { name }
    )
    return response.data
  } catch (error) {
    console.error(error)
    const axiosError = error as AxiosError
    notificationStore.triggerNotification({
      content: axiosError
    });
    return null
  }
}

export async function updateLineName(
  lineId: number,
  newName: string
): Promise<ILine | null> {
  try {
    const response = await api.put<ILine>(
      `/line/update/${lineId}`,
      { name: newName }
    )
    return response.data
  } catch (error) {
    console.error(error)
    const axiosError = error as AxiosError
    notificationStore.triggerNotification({
      content: axiosError
    });
    return null
  }
}

export async function deleteLine(
  lineId: number
): Promise<ILine | null> {
  try {
    const response = await api.delete<ILine>(
      `/line/delete/${lineId}`
    )
    return response.data
  } catch (error) {
    console.error(error)
    const axiosError = error as AxiosError
    notificationStore.triggerNotification({
      content: axiosError
    });
    return null
  }
}
