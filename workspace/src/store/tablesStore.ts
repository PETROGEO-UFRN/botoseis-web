import { create } from 'zustand'

import {
  listHelperFiles,
  createHelperFile
} from 'services/helperFileServices'

interface ITablesStoreState {
  tables: Array<IfileLink>
  loadTables: (projectId: number) => void
  uploadNewTableFile: (
    formData: FormData,
    projectId: number,
  ) => Promise<undefined | number>
}

export const useTablesStore = create<ITablesStoreState>((set, get) => ({
  tables: [],
  loadTables: (projectId) => {
    const data_type = "table"
    listHelperFiles(
      projectId,
      data_type
    ).then((result) => {
      if (!result)
        return
      set({ tables: result })
    })
  },
  uploadNewTableFile: (
    formData,
    projectId
  ) => {
    const data_type = "table"
    return new Promise(resolve => createHelperFile(
      projectId,
      formData,
      data_type
    ).then((result) => {
      if (!result) return
      set((state) => ({
        tables: [...state.tables, result.fileLink]
      }))
      resolve(result.fileLink.id)
    }))
  },
}))
