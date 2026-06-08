import { useEffect, useState } from 'react'

import { BOKEH_BRIDGE_METADATA_MODEL_NAME } from '@/constants/BOKEH_REACT_BRIDGE'
import { useBokehDocumentStore } from '@/stores/bokehDocumentStore'

interface IBokehMetadata {
  /** Total gathers in the file (null until known; absent in stack mode). */
  numGathers: number | null
}

/**
 * useBokehMetadata Hook
 *
 * Reads server-computed, read-only metadata (e.g. the real gather count) that
 * the backend publishes once per session through the metadata bridge model, so
 * the UI can bound itself to the actual file instead of guessing from the URL.
 */
export function useBokehMetadata(): IBokehMetadata {
  const bokehDocument = useBokehDocumentStore(state => state.bokehDocument)
  const [metadata, setMetadata] = useState<IBokehMetadata>({ numGathers: null })

  useEffect(() => {
    if (!bokehDocument) return

    const model = bokehDocument.get_model_by_name<number>(
      BOKEH_BRIDGE_METADATA_MODEL_NAME
    )
    if (!model || !('data' in model)) return

    const read = () => {
      const value = model.data.num_gathers?.[0]
      setMetadata({ numGathers: typeof value === 'number' ? value : null })
    }
    read()

    // The value is static per session, but the model may resolve slightly after
    // the document connects, so listen once for its data to populate.
    model.properties.data.change.connect(read)
    return () => {
      model.properties.data.change.disconnect(read)
    }
  }, [bokehDocument])

  return metadata
}
