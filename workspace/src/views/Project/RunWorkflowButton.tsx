import { useState } from "react"
import { useShallow } from "zustand/react/shallow"

import useNotificationStore from 'store/notificationStore'
import { useSelectedWorkflowsStore } from "store/selectedWorkflowsStore"
import { useVelanOptionsStore } from "store/velanOptionsStore"
import { useGatherKeyStore } from "store/gatherKeyStore"
import { useLogsStore } from "store/logsStore"
import { updateFile } from 'services/suFileServices'

import { CommandActionButtonStyled } from './styles'
import { StaticTabKey } from "constants/clientPrograms"

const notificationStore = useNotificationStore.getState()


export default function RunWorkflowButton() {

  const {
    singleSelectedWorkflowId,
    selectedWorkflows
  } = useSelectedWorkflowsStore(useShallow((state) => ({
    singleSelectedWorkflowId: state.singleSelectedWorkflowId,
    selectedWorkflows: state.selectedWorkflows
  })))
  const gatherKeys = useGatherKeyStore(useShallow((state) => state.gatherKeys))
  const pushNewLog = useLogsStore(useShallow(state => state.pushNewLog))

  const [isLoading, setIsLoading] = useState(false)

  const runWorkflow = () => {
    setIsLoading(true)
    if (!singleSelectedWorkflowId) return
    updateFile(singleSelectedWorkflowId).then((result) => {
      if (!result) return

      pushNewLog(singleSelectedWorkflowId, result.process_details)

      const currentWorkflow = selectedWorkflows.find((workflow) => workflow.id == singleSelectedWorkflowId)
      if (!currentWorkflow)
        return

      if (result.process_details.logMessage !== "Success")
        return notificationStore.triggerNotification({
          content: [
            `Error running workflow: ${currentWorkflow.name}`,
            result.process_details.logMessage
          ]
        });

      const postProcessingKey = currentWorkflow.post_processing_options?.key

      let vizualizerURL = `${import.meta.env.VITE_VISUALIZER_URL}/?`
      let velanURL = `${import.meta.env.VITE_VISUALIZER_URL}/velan?`

      if (postProcessingKey == StaticTabKey.Velan)
        return window.open(`${velanURL}workflowId=${result.result_workflow_id}`, '_blank')

      const gatherKeyFromStore = gatherKeys.get(singleSelectedWorkflowId)
      if (gatherKeyFromStore)
        vizualizerURL += `gather_key=${gatherKeyFromStore}&`
      window.open(`${vizualizerURL}workflowId=${result.result_workflow_id}`, '_blank')
    }).finally(() => {
      setIsLoading(false)
    })
  }

  return (
    <CommandActionButtonStyled
      color="primary"
      variant="outlined"
      onClick={runWorkflow}
      loading={isLoading}
    >
      Run workflow
    </CommandActionButtonStyled>
  )
}
