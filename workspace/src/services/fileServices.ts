import { AxiosError } from "axios"
import useNotificationStore from 'store/notificationStore';

import api from "./api"

interface IupdateFileResult {
  result_workflow_id: number
  process_details: IprocessLogs
}

const notificationStore = useNotificationStore.getState()

export async function listFiles(
  projectId: number,
): Promise<Array<IfileLink> | null> {
  try {
    const response = await api.get(
      `/su-file/list/${projectId}`
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

export async function createFile(
  projectId: number,
  formData: any,
): Promise<{ fileLink: IfileLink } | null> {
  try {
    const response = await api.post(
      `/su-file/create/${projectId}`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
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

export async function updateFile(
  workflowId: number
): Promise<IupdateFileResult | null> {
  try {
    const response = await api.put(
      `/su-file/update/${workflowId}`
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
