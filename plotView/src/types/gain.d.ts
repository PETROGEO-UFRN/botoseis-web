interface IAutomaticGainOptions {
  AGC: number | null
  GAUSSIAN_AGC: number | null
}

interface IGainOptions extends IAutomaticGainOptions {
  PERCENTILE_CLIPPING: number
}

interface IGainInputs {
  AUTOMATIC_GAIN: number
  PERCENTILE_CLIPPING: number
}

interface IGainOption {
  key: keyof IGainInputs
  label: string
}

type ColormapType =
  | 'grey'
  | 'red_black'
  | 'red_blue'
  | 'blue_red'
  | 'BuRd'
  | 'RdGy'
