export interface IstaticTab {
  id: StaticTabKey,
  name: string
  parameters: string
}

type staticTabsType = Array<IstaticTab>

export enum StaticTabKey {
  Input = "tab-input",
  Output = "tab-output",
  Vizualizer = "tab-vizualizer",
}


export const preProcessingCommands: staticTabsType = [
  {
    id: StaticTabKey.Input,
    name: "Input",
    parameters: ""
  }
]

export const postProcessingCommands: staticTabsType = [
  {
    id: StaticTabKey.Output,
    name: "Output",
    parameters: ""
  },
  {
    id: StaticTabKey.Vizualizer,
    name: "Visualization",
    parameters: ""
  }
]
