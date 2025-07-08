import { create } from 'zustand'


interface ILogsStore {
  logs: Map<number, Array<IprocessLogs>>
  pushNewLog: (workflowId: number, newLog: IprocessLogs) => void
}

export const useLogsStore = create<ILogsStore>((set) => ({
  logs: new Map(),
  pushNewLog: (workflowId, newLog) => {
    set((state) => {
      const tempLogs = new Map(state.logs)
      let workflowLogs = tempLogs.get(workflowId)
      if (!workflowLogs)
        workflowLogs = []

      // ! must check on programs where the output is an text output 
      if (newLog.returncode == 0)
        newLog.logMessage = "Success"

      workflowLogs.push(newLog)

      tempLogs.set(workflowId, workflowLogs)
      return { logs: tempLogs }
    })
  }
}))
