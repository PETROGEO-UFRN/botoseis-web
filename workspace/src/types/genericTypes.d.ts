declare interface IobjectWithDynamicFields<T = string | number | boolean> {
  [key: string]: T
}

declare type genericSetterType<T> = Dispatch<SetStateAction<Array<T>>> | ((newValue: Array<T>) => void)
