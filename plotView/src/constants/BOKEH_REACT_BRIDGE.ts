export const BOKEH_BRIDGE_MODEL_NAME = 'BRIDGE_ACTIONS_TRIGGER_MODEL'
export const BOKEH_BRIDGE_FEEDBACK_MODEL_NAME = 'BRIDGE_FEEDBACK_MODEL'
export const BOKEH_BRIDGE_METADATA_MODEL_NAME = 'BRIDGE_METADATA_MODEL'

export const COLORMAP_OPTIONS: Array<{ id: ColormapType; label: string }> = [
  { id: 'grey', label: 'Greyscale' },
  { id: 'red_black', label: 'Red-Black' },
  { id: 'red_blue', label: 'Red-Blue (darker)' },
  { id: 'blue_red', label: 'Blue-Red (darker)' },
  { id: 'BuRd', label: 'Blue-Red (BuRd)' },
  { id: 'RdGy', label: 'Red-Grey (RdGy)' }
]

export const AUTOMATIC_GAIN_TYPE_OPTIONS: Array<{
  id: keyof IAutomaticGainOptions | 'None'
  label: string
}> = [
  { id: 'None', label: 'None' },
  { id: 'AGC', label: 'AGC' },
  { id: 'GAUSSIAN_AGC', label: 'Gaussian AGC' }
]

export const GAIN_OPTIONS: Array<IGainOption> = [
  { key: 'AUTOMATIC_GAIN', label: 'Automatic Gain (window, s)' },
  { key: 'PERCENTILE_CLIPPING', label: 'Percentile Clipping' }
]
