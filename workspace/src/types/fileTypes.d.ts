declare type helperFileTypes = "model" | "table"

declare interface IfileLink {
  id: number
  name: string
  data_type: ".su" | helperFileTypes
  projectId: number | undefined
  datasetId: number | undefined
}
