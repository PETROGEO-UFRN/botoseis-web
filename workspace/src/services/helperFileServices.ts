import { AxiosError } from "axios"
import useNotificationStore from 'store/notificationStore'

import api from "./api"

const notificationStore = useNotificationStore.getState()

export async function listHelperFiles(
  lineId: number,
  data_type: helperFileTypes
): Promise<Array<IfileLink> | null> {
  try {
    const response = await api.get(
      `/helper-file/list/${lineId}/${data_type}s`
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

export async function createHelperFile(
  lineId: number,
  formData: any,
  data_type: helperFileTypes
): Promise<{ fileLink: IfileLink } | null> {
  try {
    const response = await api.post(
      `/helper-file/upload/${lineId}/${data_type}`,
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
