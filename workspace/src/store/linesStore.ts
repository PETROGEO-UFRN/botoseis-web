import { create } from 'zustand'

import {
  getLinesByProjectID,
  createNewLine,
  updateLineName,
  deleteLine,
} from 'services/lineServices'

import {
  createNewWorkflow,
  updateWorkflowName,
  deleteWorkflow,
} from 'services/workflowServices'

type linesType = Array<ILine>

interface ILinesStoreState {
  lines: linesType
  loadLines: (projectId: number) => void
  saveNewLine: (projectId: number, name: string) => void
  updateLineName: (lineId: number, newName: string) => void
  removeLine: (lineId: number) => void

  // ! Workflows are too acoplated to lines store
  // ! Deacoplate may cost performance
  pushNewWorkflowToLine: (lineId: number, name: string) => void
  updateWorkflowName: (lineId: number, workflowId: number, newName: string) => void
  removeWorkflowFromLine: (lineId: number, workflowId: number) => void
}

export const useLinesStore = create<ILinesStoreState>((set) => ({
  lines: [],
  loadLines: (projectId: number) => {
    getLinesByProjectID(projectId)
      .then((result) => {
        if (Array.isArray(result))
          set({ lines: result })
      })
  },
  saveNewLine: (projectId: number, name: string) => {
    createNewLine(projectId, name)
      .then(result => {
        if (!result)
          return
        set((state) => ({ lines: [...state.lines, result] }))
      })
  },
  updateLineName: (lineId: number, newName: string) => {
    updateLineName(lineId, newName)
      .then(result => {
        if (!result)
          return
        set((state) => ({
          lines: state.lines.map((line) => {
            if (line.id == lineId)
              line.name = newName
            return line
          })
        }))
      })
  },
  removeLine: (lineId: number) => {
    deleteLine(lineId).then(result => {
      if (!result)
        return
      set((state) => ({
        lines: state.lines.filter((line) => line.id != lineId)
      }))
    })
  },
  pushNewWorkflowToLine: (lineId: number, name: string) => {
    createNewWorkflow(lineId, "lineId", name)
      .then(result => {
        if (!result)
          return
        set((state) => ({
          lines: state.lines.map((line) => {
            if (line.id == lineId)
              line.workflows.push(result)
            return line
          })
        }))
      })
  },
  updateWorkflowName: (lineId, workflowId, newName) => {
    updateWorkflowName(workflowId, newName).then(result => {
      if (!result)
        return
      set((state) => ({
        lines: state.lines.map((line) => {
          if (line.id == lineId)
            line.workflows = line.workflows.map((workflow) => {
              if (workflow.id == workflowId)
                workflow.name = newName
              return workflow
            })
          return line
        })
      }))
    })
  },
  removeWorkflowFromLine: (lineId: number, workflowId: number) => {
    deleteWorkflow(workflowId).then(result => {
      if (!result)
        return
      set((state) => ({
        lines: state.lines.map((line) => {
          if (line.id == lineId)
            line.workflows = line.workflows.filter((workflow) => workflow.id != workflowId)
          return line
        })
      }))
    })
  },
}))
