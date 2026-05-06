import { useEffect, useRef } from 'react'
import { useDebouncedCallback, useThrottledCallback } from 'use-debounce'
import {
  BOKEH_BRIDGE_FEEDBACK_MODEL_NAME,
  BOKEH_BRIDGE_MODEL_NAME
} from '@/constants/BOKEH_REACT_BRIDGE'
import { useBokehDocumentStore } from '@/stores/bokehDocumentStore'

interface IPendingPromises {
  resolve: (value: IEmptyApiResponse) => void
  reject: (reason: IEmptyApiResponse) => void
}

type DebouncedTriggerPropsType = {
  [K in keyof IBridgeValidActions]: { [Key in K]: IBridgeValidActions[K] }
}[keyof IBridgeValidActions]

const DEBOUNCE_TIME_MS = 500
/** THROTTLE running arround 30fps */
const THROTTLE_TIME_IN_MS = 41

/**
 * useBokeh Hook
 *
 * Safely locates a Bokeh document based on a known model name.
 *
 * Provides triggers to update data on bokeh server.
 */
export function useBokeh() {
  const bokehDocument = useBokehDocumentStore(state => state.bokehDocument)
  const pendingPromises = useRef<Map<string, IPendingPromises>>(new Map())
  const newValuesBufferRef = useRef<IBridgeValidActions>({})

  /**
   * Triggers a Bokeh model update (on Bokeh ColumnDataSource).
   * ColumnDataSource updates can be used to trigger action on server-side.
   *
   * Block too many requests in a short time, ignoring exceeding calls
   */
  const emitThrottledTrigger = useThrottledCallback(
    newValues => emitTrigger(newValues),
    THROTTLE_TIME_IN_MS,
    { leading: true }
  )

  const debouncedTrigger = useDebouncedCallback(() => {
    const newValues = newValuesBufferRef.current
    newValuesBufferRef.current = {}
    emitTrigger(newValues)
  }, DEBOUNCE_TIME_MS)

  /**
   * Triggers a Bokeh model update (on Bokeh ColumnDataSource).
   * ColumnDataSource updates can be used to trigger action on server-side.
   *
   * Accumulate requests when too many calls are made in a short period to request all at once.
   */
  const emitDebouncedTrigger = (
    newValues: DebouncedTriggerPropsType
  ): Promise<IEmptyApiResponse> => {
    if (!newValues) return Promise.resolve({ ok: true })

    Object.assign(newValuesBufferRef.current, newValues)
    return new Promise((resolve, reject) => {
      debouncedTrigger()
      const key = Object.keys(newValues)[0]
      // *** Reset pending promise for the key when new value is emitted
      pendingPromises.current.get(key)?.resolve({ ok: false })
      pendingPromises.current.set(key, { resolve, reject })
    })
  }

  /**
   * Triggers a Bokeh model update (on Bokeh ColumnDataSource).
   * ColumnDataSource updates can be used to trigger action on server-side.
   */
  const emitTrigger = (newValues: IBridgeValidActions) => {
    if (!bokehDocument)
      return console.warn('[useBokeh]: Document not ready yet.')
    if (!newValues) return

    const trigger =
      bokehDocument.get_model_by_name<PackedBridgeValidActionsType>(
        BOKEH_BRIDGE_MODEL_NAME
      )
    if (!trigger) return console.error('[useBokeh]: trigger not found')
    if (!('data' in trigger))
      return console.error('[useBokeh]: trigger has no data')

    const newValuesWrapped = Object.fromEntries(
      Object.entries(newValues).map(([key, value]) => [key, [value]])
    )

    trigger.data = { ...newValuesWrapped }
    trigger.change.emit()
  }

  useEffect(() => {
    if (!bokehDocument)
      return console.warn('[useBokeh]: Document not ready yet.')

    const feedbackSource = bokehDocument.get_model_by_name<boolean>(
      // *** Model for receiving trigger results from server
      BOKEH_BRIDGE_FEEDBACK_MODEL_NAME
    )
    if (!feedbackSource)
      return console.warn('[useBokeh]: feedbackSource not found in document.')
    if (!('data' in feedbackSource))
      return console.error('[useBokeh]: feedbackSource has no data')

    const endPromise = () => {
      const data = feedbackSource.data
      Object.keys(data).forEach(key => {
        const pendingPromise = pendingPromises.current.get(key)
        if (!pendingPromise) return
        pendingPromise.resolve({ ok: true })
        pendingPromises.current.delete(key)
      })
    }

    feedbackSource.properties.data.change.connect(endPromise)
    return () => {
      feedbackSource.properties.data.change.disconnect(endPromise)
    }
  }, [bokehDocument])

  useEffect(
    () => () => {
      debouncedTrigger.flush()
    },
    [debouncedTrigger]
  )

  return { emitTrigger, emitDebouncedTrigger, emitThrottledTrigger }
}
