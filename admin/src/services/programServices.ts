import api from "./api"

export async function getPrograms(groupId: number): Promise<Array<IGenericProgram>> {
  try {
    const response = await api.get<Array<IGenericProgram>>(`/programs/list/${groupId}`)
    return response.data
  } catch (error) {
    console.error(error)
    return []
  }
}

export async function createNewProgram(
  groupId: number,
  customProgram: FileList | null,
  programData: IGenericProgramConstructor
): Promise<IGenericProgram | null> {
  try {
    const formData = new FormData()
    Object.keys(programData).forEach((keyString) => {
      const key = keyString as GenericProgramConstructorKeysType
      formData.append(key, programData[key].toString())
    })
    if(customProgram)
      formData.append("file", customProgram[0])

    const response = await api.post<IGenericProgram>(
      `/programs/create/${groupId}`,
      programData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}

export async function updateProgram(
  programId: number,
  customProgram: FileList | null,
  programData: IGenericProgramConstructor
): Promise<IGenericProgram | null> {
  try {
    const formData = new FormData()
    Object.keys(programData).forEach((keyString) => {
      const key = keyString as GenericProgramConstructorKeysType
      formData.append(key, programData[key].toString())
    })
    if(customProgram)
      formData.append("file", customProgram[0])

    const response = await api.put<IGenericProgram>(
      `/programs/update/${programId}`,
      programData,
      {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }
    )
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}

export async function deleteProgram(programId: number): Promise<IGenericProgram | null> {
  try {
    const response = await api.delete(`/programs/delete/${programId}`)
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}
