import api from "./api"

// ! Duplicated ! Shall be shared from "admin" as well as its types

export async function getGroups(): Promise<Array<IProgramsGroup>> {
  try {
    const response = await api.get<Array<IProgramsGroup>>(`/programs/groups/list`)
    return response.data
  } catch (error) {
    console.error(error)
    return []
  }
}

export async function getPrograms(groupId: number): Promise<Array<IseismicProgram>> {
  try {
    const response = await api.get<Array<IseismicProgram>>(`/programs/list/${groupId}`)
    return response.data
  } catch (error) {
    console.error(error)
    return []
  }
}

export async function getParameters(programId: number): Promise<Array<IParameter>> {
  try {
    const response = await api.get<Array<IParameter>>(`/programs/parameters/list/${programId}`)
    return response.data
  } catch (error) {
    console.error(error)
    return []
  }
}

