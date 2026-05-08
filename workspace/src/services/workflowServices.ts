import { AxiosError } from "axios"

import useNotificationStore from 'store/notificationStore';
import { defaultOutputName } from 'constants/defaults'

import api from "./api"

interface IupdateWorkflowPostProcessingProps {
  workflowId: number,
  key: IpostProcessingOptions["key"],
  options?: IpostProcessingOptions["options"],
}

type postProcessingReturnType = Pick<IWorkflow, "post_processing_options">

const notificationStore = useNotificationStore.getState()

export async function getWorkflowByID(
  id: number,
): Promise<IWorkflow | null> {
  try {
    const response = await api.get<IWorkflow>(
      `/workflow/show/${id}`
    )
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

export async function createNewWorkflow(
  parentId: number,
  parentType: "projectId" | "lineId",
  name: string,
): Promise<IResumedWorkflow | null> {
  try {
    const response = await api.post<IResumedWorkflow>(
      `/workflow/create/${parentId}`,
      {
        parentType,
        name,
        output_name: defaultOutputName
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

export async function updateWorkflowName(
  workflowId: number,
  name: string,
): Promise<IWorkflow | null> {
  try {
    const response = await api.put<IWorkflow>(
      `/workflow/update/${workflowId}/name`,
      {
        name
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

export async function updateWorkflowFileLink(
  workflowId: number,
  fileLinkId: number,
): Promise<IWorkflow | null> {
  try {
    const response = await api.put<IWorkflow>(
      `/workflow/update/${workflowId}/file`,
      {
        fileLinkId
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

export async function updateWorkflowOutputName(
  workflowId: number,
  outputName: string,
): Promise<IWorkflow | null> {
  try {
    const response = await api.put<IWorkflow>(
      `/workflow/update/${workflowId}/output-name`,
      {
        outputName
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


export async function updateWorkflowPostProcessing({
  workflowId,
  key,
  options = {},
}: IupdateWorkflowPostProcessingProps): Promise<postProcessingReturnType | null> {
  try {
    const response = await api.put<postProcessingReturnType>(
      `/workflow/update/${workflowId}/post-processing`,
      {
        key,
        options,
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

export async function deleteWorkflow(
  workflowId: number,
): Promise<IWorkflow | null> {
  try {
    const response = await api.delete<IWorkflow>(
      `/workflow/delete/${workflowId}`
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
