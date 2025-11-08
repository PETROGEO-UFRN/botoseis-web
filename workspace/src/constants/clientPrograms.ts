
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
