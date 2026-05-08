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
  Velan = "tab-Velan",
}

const clientProgramsGroupID = "client-side-programs"
const sharedClientProgramsParameters: Pick<
  IGenericProgram,
  'path_to_executable_file' | 'groupId'
> = {
  path_to_executable_file: "",
  groupId: clientProgramsGroupID,
}

const clientPrograms: Array<IGenericProgram<clientProgramIdType>> = [
  {
    id: StaticTabKey.Vizualizer,
    name: "Visualization",
    description: "Data visualization. Wiggle view & Image view.",
    ...sharedClientProgramsParameters,
  },
  {
    id: StaticTabKey.Velan,
    name: "Velocity Analysis",
    description: "Interative Velocity Analysis programs.",
    ...sharedClientProgramsParameters,
  }
]

export const clientProgramsGroup: IProgramsGroup<clientProgramIdType> = {
  id: clientProgramsGroupID,
  name: "Plotting",
  description: "",
  programs: clientPrograms,
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
  },
  {
    id: StaticTabKey.Velan,
    name: "Velocity Analysis",
    parameters: ""
  }
]
