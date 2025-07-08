import { create } from 'zustand'

import { getWorkflowByID } from 'services/workflowServices'

type selectedWorkflowsType = Array<IWorkflow>
type singleSelectedWorkflowIdType = number | undefined

interface ISelectedWorkflowsStoreState {
  selectedWorkflows: selectedWorkflowsType
  // todo: "singleSelectedWorkflowId" shall be converted to "singleSelectedWorkflow"
  // *** this will improve performance by not needing many forEachs to get selectedWorkflow info  
  // *** at some components.
  singleSelectedWorkflowId: singleSelectedWorkflowIdType
  hasSelectedDataset: boolean
  setSelectedWorkflows: (newWorkflows: selectedWorkflowsType) => void
  setSingleSelectedWorkflowId: (newWorkflowId: singleSelectedWorkflowIdType) => void
  selectWorkflow: (
    workflowId: number,
    afterSelect: () => any
  ) => void
}

export const useSelectedWorkflowsStore = create<ISelectedWorkflowsStoreState>((set, get) => ({
  selectedWorkflows: [],
  singleSelectedWorkflowId: undefined,
  hasSelectedDataset: false,

  setSelectedWorkflows: (newWorkflow) =>
    set({ selectedWorkflows: newWorkflow }),
  setSingleSelectedWorkflowId: (newWorkflowId) => {
    let newHasSelectedDataset = false;
    if (newWorkflowId) {
      const workflowToSelect = get().selectedWorkflows.find((workflow) => workflow.id == newWorkflowId)
      if (workflowToSelect && workflowToSelect.parentType == 'dataset')
        newHasSelectedDataset = true
    }
    set({
      singleSelectedWorkflowId: newWorkflowId,
      hasSelectedDataset: newHasSelectedDataset,
    })
  },

  selectWorkflow: (workflowId: number, afterSelect) => {
    if (get().singleSelectedWorkflowId != undefined) {
      const isAlredySingleSelected = workflowId == get().singleSelectedWorkflowId;
      if (isAlredySingleSelected)
        return
    }


    const selectedWorkflowIndex = get().selectedWorkflows.findIndex(
      (element) => element.id == workflowId
    )
    const isAlredySelected = selectedWorkflowIndex >= 0

    if (isAlredySelected) {
      let newHasSelectedDataset = false;
      if (get().selectedWorkflows[selectedWorkflowIndex].parentType == 'dataset')
        newHasSelectedDataset = true

      set({
        singleSelectedWorkflowId: workflowId,
        hasSelectedDataset: newHasSelectedDataset
      })
      afterSelect()
      return
    }

    getWorkflowByID(workflowId)
      .then(result => {
        if (!result) return

        let newHasSelectedDataset = false;
        if (result.parentType == 'dataset') newHasSelectedDataset = true

        set((state) => ({
          hasSelectedDataset: newHasSelectedDataset,
          singleSelectedWorkflowId: result.id,
          selectedWorkflows: [
            ...state.selectedWorkflows,
            {
              id: result.id,
              name: result.name,
              input_file_link_id: result.input_file_link_id,
              commands: result.commands,
              output_name: result.output_name,
              parentType: result.parentType,
            },
          ]
        }))
        afterSelect()
      })
  }
}))
