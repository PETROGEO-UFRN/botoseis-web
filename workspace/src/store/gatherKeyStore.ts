import { create } from 'zustand'

interface IGatherKeyStore {
  gatherKeys: Map<number, string>
  updateGatherKey: (workflowId: number | undefined, newGatherKey: string) => void
}

export const useGatherKeyStore = create<IGatherKeyStore>((set) => ({
  gatherKeys: new Map(),
  updateGatherKey: (workflowId, newGatherKey) => {
    if (!workflowId)
      return
    set((state) => {
      const tempGatherKeys = new Map(state.gatherKeys)
      tempGatherKeys.set(workflowId, newGatherKey)
      return { gatherKeys: tempGatherKeys }
    })
  }
}))
