import { create } from 'zustand'

interface IBokehDocumentStore {
  bokehDocument: BokehDocumentType | null
  setBokehDocument: (document: BokehDocumentType | null) => void
}

export const useBokehDocumentStore = create<IBokehDocumentStore>(set => ({
  bokehDocument: null,
  setBokehDocument: document => set({ bokehDocument: document })
}))
