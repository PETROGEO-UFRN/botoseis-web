import { useState } from "react"
import { useShallow } from "zustand/react/shallow"

import { useSelectedWorkflowsStore } from "store/selectedWorkflowsStore"
import { useGatherKeyStore } from "store/gatherKeyStore"
import { useLogsStore } from "store/logsStore"
import { updateFile } from 'services/fileServices'

import { CommandActionButtonStyled } from './styles'

export default function RunWorkflowButton() {
  const singleSelectedWorkflowId = useSelectedWorkflowsStore(useShallow((state) => (
    state.singleSelectedWorkflowId
  )))
  const gatherKeys = useGatherKeyStore(useShallow((state) => state.gatherKeys))
  const pushNewLog = useLogsStore(useShallow(state => state.pushNewLog))

  const [isLoading, setIsLoading] = useState(false)

  const runWorkflow = () => {
    setIsLoading(true)
    if (!singleSelectedWorkflowId) return
    updateFile(singleSelectedWorkflowId).then((result) => {
      if (!result) return

      pushNewLog(singleSelectedWorkflowId, result.process_details)

      let vizualizerURL = `${import.meta.env.VITE_VISUALIZER_URL}/?`
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
