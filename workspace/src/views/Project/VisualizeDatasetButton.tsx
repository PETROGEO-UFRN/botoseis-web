import { useState } from "react"
import { useShallow } from "zustand/react/shallow"

import { useGatherKeyStore } from "store/gatherKeyStore"
import { useSelectedWorkflowsStore } from "store/selectedWorkflowsStore";

import { CommandActionButtonStyled } from "./styles";

export default function VisualizeDatasetButton() {
  const singleSelectedWorkflowId = useSelectedWorkflowsStore(useShallow((state) => (
    state.singleSelectedWorkflowId
  )))
  const gatherKeys = useGatherKeyStore(useShallow((state) => state.gatherKeys))

  const [isLoading, setIsLoading] = useState(false)

  const displayDataset = () => {
    setIsLoading(true)
    if (!singleSelectedWorkflowId) return

    let vizualizerURL = `${import.meta.env.VITE_VISUALIZER_URL}/?`
    const gatherKeyFromStore = gatherKeys.get(singleSelectedWorkflowId)
    if (gatherKeyFromStore)
      vizualizerURL += `gather_key=${gatherKeyFromStore}&`

    window.open(`${vizualizerURL}workflowId=${singleSelectedWorkflowId}`, '_blank')

    setIsLoading(false)
  }

  return (
    <CommandActionButtonStyled
      color="primary"
      variant="outlined"
      onClick={displayDataset}
      loading={isLoading}
    >
      Visualize Dataset
    </CommandActionButtonStyled>
  )
}
