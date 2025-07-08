declare interface IobjectWithDynamicFields {
  [key: string]: string | number | boolean
}

declare type genericSetterType<T> = Dispatch<SetStateAction<Array<T>>> | ((newValue: Array<T>) => void)
