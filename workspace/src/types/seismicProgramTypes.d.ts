type parameterFileInputType = `file:${helperFileTypes}`

declare interface IseismicProgramParameters {
  id: number
  name: string
  description: string
  input_type: "float" | "integer" | "string" | parameterFileInputType
  isRequired: boolean
}

declare interface IseismicProgram {
  id: number
  name: string
  description: string
}
