import api from "./api"

export async function getGroups(): Promise<Array<IProgramsGroup>> {
  try {
    const response = await api.get<Array<IProgramsGroup>>(`/programs/groups/list`)
    return response.data
  } catch (error) {
    console.error(error)
    return []
  }
}

export async function createNewGroup(groupData: IProgramsGroupConstructor): Promise<IProgramsGroup | null> {
  try {
    const response = await api.post<IProgramsGroup>(`/programs/groups/create`, {
      ...groupData
    })
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}

export async function deleteGroup(groupId: number): Promise<IProgramsGroup | null> {
  try {
    const response = await api.delete(`/programs/groups/delete/${groupId}`)
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}
