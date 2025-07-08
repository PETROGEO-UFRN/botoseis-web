interface IfileLink {
  id: number
  name: string
  data_type: "su" | "asc_table" | "velocity_model"
  projectId: number | undefined
  datasetId: number | undefined
}
