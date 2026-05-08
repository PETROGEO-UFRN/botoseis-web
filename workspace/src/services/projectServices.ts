import { AxiosError } from "axios"
import useNotificationStore from 'store/notificationStore';

import api from "./api"

const notificationStore = useNotificationStore.getState()

export async function getProjectsByUser(): Promise<Array<IProject> | null> {
  try {
    const response = await api.get<Array<IProject>>(`/project/list`)
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

export async function createNewProject(name: string): Promise<IProject | null> {
  try {
    const response = await api.post<IProject>(
      `/project/create`,
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

export async function deleteProject(id: number): Promise<IProject | null> {
  try {
    const response = await api.delete<IProject>(
      `/project/delete/${id}`
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
