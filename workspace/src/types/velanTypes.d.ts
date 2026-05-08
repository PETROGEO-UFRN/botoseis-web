declare interface IvelanOptions {
  first_cdp: number | null
  last_cdp: number | null
  number_of_gathers_per_time: number | null
  first_velocity_value: number | null
  last_velocity_value: number | null
  velocity_step_size: number | null
}

declare type velanOptionKeyType = keyof IvelanOptions;
