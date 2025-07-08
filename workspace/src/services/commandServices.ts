import { AxiosError } from "axios"
import useNotificationStore from 'store/notificationStore';
import { StaticTabKey } from 'constants/StaticTabKey'

import api from "./api"

const notificationStore = useNotificationStore.getState()

export async function createNewCommand(
  workflowId: number,
  program_id: number,
  name: string,
): Promise<ICommand | null> {
  try {
    const response = await api.post<ICommand>(
      `/command/create/${workflowId}`,
      {
        name,
        program_id,
        parameters: "{}"
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

export async function updateCommandParameters(
  // ! id type must be reviewed, StaticTabKey would cause errors
  id: number | StaticTabKey,
  newParameters: string
): Promise<ICommand | null> {
  try {
    const response = await api.put<ICommand>(
      `/command/update/${id}/parameters`,
      {
        parameters: newParameters
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

export async function updateCommandIsActive(
  // ! id type must be reviewed, StaticTabKey would cause errors
  id: number | StaticTabKey,
): Promise<ICommand | null> {
  try {
    const response = await api.put<ICommand>(
      `/command/update/${id}/is_active`,
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

export async function updateCommandsOrder(
  workflowId: string,
  newOrder: idsType
): Promise<orderedCommandsListType | null> {
  try {
    const response = await api.put<orderedCommandsListType>(
      `/command/order/${workflowId}`,
      { newOrder }
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

export async function deleteCommand(
  commandId: string,
): Promise<ICommand | null> {
  try {
    const response = await api.delete<ICommand>(
      `/command/delete/${commandId}`
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
