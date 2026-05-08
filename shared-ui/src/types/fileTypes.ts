export interface IfileLink {
  id: number
  name: string
  data_type: "su" | "table" | "model"
  projectId: number | undefined
  datasetId: number | undefined
}
