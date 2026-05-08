import { createContext, useContext, useState, useEffect } from 'react'
import type { ReactNode } from 'react'
import { getGroups, createNewGroup, deleteGroup } from '../services/programGroupServices'

interface IGroupsProviderProps {
  children: ReactNode | Array<ReactNode>
}

interface IGroupsContext {
  programGroups: Array<IProgramsGroup>
  createProgramGroup: (newGroupData: IProgramsGroupConstructor) => undefined | void
  deleteProgramGroup: (groupId: number) => undefined | void
  addNewProgramOnGroup: (program: IGenericProgram) => undefined | void
  updateProgramOnGroup: (program: IGenericProgram) => undefined | void
}

const GroupsContext = createContext<IGroupsContext>({
  programGroups: [],
  createProgramGroup: () => undefined,
  deleteProgramGroup: () => undefined,
  addNewProgramOnGroup: () => undefined,
  updateProgramOnGroup: () => undefined,
});

export default function GroupsProvider({ children }: IGroupsProviderProps) {
  const [programGroups, setProgramGroups] = useState< Array<IProgramsGroup> >([])

  const createProgramGroup = (newGroupData: IProgramsGroupConstructor) => {
    createNewGroup(newGroupData).then(newGroup => newGroup && setProgramGroups([...programGroups, newGroup]))
  }

  const deleteProgramGroup = (groupId: number) => {
    deleteGroup(groupId).then((responseData) => {
      if(responseData) {
        const newProgramGroups = [...programGroups].filter(
          oldGroup => oldGroup.id !== groupId
        )
        setProgramGroups(newProgramGroups)
      }
    })
  }

  const addNewProgramOnGroup = (newProgram: IGenericProgram) => {
    const tempProgramGroups = programGroups.map((group) => {
      if(group.id == newProgram.groupId)
        group.programs.push(newProgram)
      return group
    })
    setProgramGroups(tempProgramGroups)
  }

  const updateProgramOnGroup = (updatedProgram: IGenericProgram) => {
    const tempProgramGroups = programGroups.map((group) => {
      if(group.id == updatedProgram.groupId)
        group.programs = group.programs.map((program) => {
          if(program.id == updatedProgram.id)
            program = updatedProgram
          return program
        })
        return group
    })
    setProgramGroups(tempProgramGroups)
  }

  useEffect(() => {
    getGroups().then(allGroups => allGroups && setProgramGroups(allGroups))
  }, [])

  return (
    <GroupsContext.Provider
      value={{
        programGroups,
        createProgramGroup,
        deleteProgramGroup,
        addNewProgramOnGroup,
        updateProgramOnGroup
      }}
    >
      {children}
    </GroupsContext.Provider>
  )
}

// eslint-disable-next-line react-refresh/only-export-components
export function useProgramGroups(): IGroupsContext {
  const context = useContext(GroupsContext)
  if (!context)
    throw new Error('useProgramGroups must be used within a GroupsProvider')
  const {
    programGroups,
    createProgramGroup,
    deleteProgramGroup,
    addNewProgramOnGroup,
    updateProgramOnGroup,
  } = context
  return {
    programGroups,
    createProgramGroup,
    deleteProgramGroup,
    addNewProgramOnGroup,
    updateProgramOnGroup,
  }
}
