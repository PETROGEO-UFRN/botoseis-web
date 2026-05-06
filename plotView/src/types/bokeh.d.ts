import type { ColumnDataSource, Document } from '@bokeh/bokehjs'

interface IModelChangeEvent {
  emit: () => void
  connect: (
    slot: (...args: unknown[]) => void,
    context?: object | null
  ) => boolean
  disconnect: (
    slot: (...args: unknown[]) => void,
    context?: object | null
  ) => boolean
}

interface IGetModelByNameReturnType<T> {
  data: T extends object ? T : Record<string, T[]>
  change: IModelChangeEvent
  properties: {
    data: {
      change: IModelChangeEvent
    }
  }
}

declare global {
  type BokehColumnDataSourceType = ColumnDataSource

  type BokehDocumentType = Omit<Document, 'get_model_by_name'> & {
    get_model_by_name<T = unknown>(
      name: string
    ): IGetModelByNameReturnType<T> | null
  }

  interface Window {
    Bokeh?: {
      documents?: BokehDocumentType[]
    }
  }
}
