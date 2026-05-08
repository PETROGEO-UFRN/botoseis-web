import api from "./api"

export async function getParameters(parameterId: number): Promise<Array<IParameter>> {
  try {
    const response = await api.get<Array<IParameter>>(`/programs/parameters/list/${parameterId}`)
    return response.data
  } catch (error) {
    console.error(error)
    return []
  }
}

export async function createNewParameter(
  programId: number
): Promise<IParameter | null> {
  try {
    const response = await api.post<IParameter>(`/programs/parameters/create/${programId}`)
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}

export async function updateParameter(
  parameterInfo: IParameter
): Promise<IParameter | null> {
  try {
    const response = await api.put<IParameter>(`/programs/parameters/update/${parameterInfo.id}`, {
      name: parameterInfo.name,
      description: parameterInfo.description,
      example: parameterInfo.example,
      input_type: parameterInfo.input_type,
      isRequired: parameterInfo.isRequired,
    })
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}

export async function deleteParameter(parameterId: number): Promise<IParameter | null> {
  try {
    const response = await api.delete(`/programs/parameters/delete/${parameterId}`)
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}
