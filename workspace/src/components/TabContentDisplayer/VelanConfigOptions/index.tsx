import { FormEvent } from "react"
import { useShallow } from "zustand/react/shallow"
import Button from "@mui/material/Button"

import { StaticTabKey } from "constants/clientPrograms"
import { updateWorkflowPostProcessing } from "services/workflowServices"
import { useSelectedWorkflowsStore } from "store/selectedWorkflowsStore"
import { useVelanOptionsStore } from "store/velanOptionsStore"

import {
  Container,
  CustomTextField
} from "./styles"


export default function VelanConfigOptions() {
  const {
    velanOptions,
    updateVelanOption,
  } = useVelanOptionsStore(useShallow(state => ({
    velanOptions: state.velanOptions,
    updateVelanOption: state.updateVelanOption
  })))

  const {
    singleSelectedWorkflowId
  } = useSelectedWorkflowsStore(useShallow(state => ({
    singleSelectedWorkflowId: state.singleSelectedWorkflowId
  })))

  const handleVelanOptionsUpdate = (event: FormEvent) => {
    event.preventDefault()
    if (!singleSelectedWorkflowId)
      return
    updateWorkflowPostProcessing({
      workflowId: singleSelectedWorkflowId,
      key: StaticTabKey.Velan,
      options: velanOptions,
    })
  }

  return (
    <Container onSubmit={handleVelanOptionsUpdate}>
      {(Object.entries(velanOptions) as [velanOptionKeyType, number][]).map(([key, value]) => (
        <CustomTextField
          key={key}
          label={key.replaceAll('_', ' ')}
          value={value}
          onChange={(event) => updateVelanOption(
            key,
            event.target.value ? Number(event.target.value) : null
          )}
          type="number"
          size="small"
          slotProps={{
            inputLabel: {
              shrink: true,
            },
          }}
        />
      ))}

      <Button
        type="submit"
        variant='contained'
      >
        Save Velan Options
      </Button>
    </Container>
  )
}
