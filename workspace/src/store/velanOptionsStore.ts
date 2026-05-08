import { create } from 'zustand'

interface IVelanOptionsStore {
  velanOptions: IvelanOptions | {}
  unpackVelanOptions: (workflow: IWorkflow) => void
  updateVelanOption: (
    optionKey: velanOptionKeyType,
    newValue: number | null
  ) => void
}

export const useVelanOptionsStore = create<IVelanOptionsStore>((set) => ({
  velanOptions: {
    first_cdp: null,
    last_cdp: null,
    number_of_gathers_per_time: null,
    first_velocity_value: null,
    last_velocity_value: null,
    velocity_step_size: null,
  },
  unpackVelanOptions: (workflow) => {
    const tempOptions = workflow.post_processing_options?.options

    const defaultVelanOptions = {
      first_cdp: null,
      last_cdp: null,
      number_of_gathers_per_time: null,
      first_velocity_value: null,
      last_velocity_value: null,
      velocity_step_size: null,
    }

    set({
      velanOptions: {
        ...defaultVelanOptions,
        ...tempOptions
      }
    })
  },
  updateVelanOption: (optionKey, newValue) => {
    set((state) => {
      const tempVelanOptions = { ...state.velanOptions }
      tempVelanOptions[optionKey] = newValue
      return { velanOptions: tempVelanOptions }
    })
  },
}))
