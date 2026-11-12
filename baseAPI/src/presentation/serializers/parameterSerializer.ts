import type { IParameter } from '@/models/index'

export function serializeParameter(parameter: IParameter) {
  return {
    id: parameter.id,
    name: parameter.name,
    description: parameter.description,
    example: parameter.example,
    input_type: parameter.inputType,
    isRequired: parameter.isRequired
  }
}
