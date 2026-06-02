import type { RefObject } from 'react'
import { useCallback } from 'react'
import { BOKEH_BRIDGE_MODEL_NAME } from '@/constants/BOKEH_REACT_BRIDGE'
import type { PLOT_TYPES_ENUM } from '@/constants/PLOT_TYPES'
import { getPlotScript } from '@/services/plotScriptServices'
import { useBokehDocumentStore } from '@/stores/bokehDocumentStore'

const RETRY_MS = 500
const MAX_RESOLVE_ATTEMPTS = 120

interface ILoadBokehScriptsReturn {
  ok: boolean
}

interface ILoadBokehScriptsProps {
  plotType: PLOT_TYPES_ENUM
  workflowId: string
  origin?: OriginType
  setupProps?: plotSetupPropsType
}

export function useBokehLoader(containerRef: RefObject<HTMLDivElement | null>) {
  const setBokehDocument = useBokehDocumentStore(
    state => state.setBokehDocument
  )

  const updateBokehPlotScript = useCallback(
    (scriptTagAsString: string) => {
      if (!containerRef.current) return

      const parser = new DOMParser()
      const virtualDocument = parser.parseFromString(
        scriptTagAsString,
        'text/html'
      )
      const scriptHTMLTag = virtualDocument.querySelector('script')

      if (!scriptHTMLTag)
        throw new Error('No <script> tag found in the provided string.')

      const newScriptTag = document.createElement('script')

      // *** Expected only id, building it future-proof by copying all attributes
      Array.from(scriptHTMLTag.attributes).forEach(attribute => {
        newScriptTag.setAttribute(attribute.name, attribute.value)
      })

      newScriptTag.textContent = scriptHTMLTag.textContent
      containerRef.current.replaceChildren(newScriptTag)
    },
    [containerRef]
  )

  const resolveBokehDocument = useCallback(async () => {
    let attempts = 0
    return await new Promise<BokehDocumentType | null>(resolve => {
      const tryResolveDocument = () => {
        if (typeof window === 'undefined' || attempts > MAX_RESOLVE_ATTEMPTS)
          return resolve(null)
        attempts += 1

        if (attempts % 10 === 1)
          console.log(`[resolveBokehDocument] attempt=${attempts} hasBokeh=${!!window.Bokeh} docCount=${window.Bokeh?.documents?.length ?? 0}`)

        if (!window.Bokeh?.documents)
          return setTimeout(tryResolveDocument, RETRY_MS)
        const document = window.Bokeh.documents.findLast(document =>
          document.get_model_by_name(BOKEH_BRIDGE_MODEL_NAME)
        )
        if (document) {
          console.log('[resolveBokehDocument] document found after', attempts, 'attempts')
          setBokehDocument(document)
          return resolve(document)
        }

        return setTimeout(tryResolveDocument, RETRY_MS)
      }

      tryResolveDocument()
    })
  }, [setBokehDocument])

  const loadBokehScripts = useCallback(
    async ({
      plotType,
      workflowId,
      origin,
      setupProps
    }: ILoadBokehScriptsProps): Promise<ILoadBokehScriptsReturn> => {
      const result = await getPlotScript({
        plotType,
        workflowId,
        origin,
        setupProps
      })

      if (!result.ok || !result.scriptTagAsString) return { ok: false }

      try {
        setBokehDocument(null)
        updateBokehPlotScript(result.scriptTagAsString)
        const document = await resolveBokehDocument()
        if (!document) return { ok: false }
        return { ok: true }
      } catch (error) {
        console.error('Script injection failed:', error)
        return { ok: false }
      }
    },
    [resolveBokehDocument, setBokehDocument, updateBokehPlotScript]
  )

  return { loadBokehScripts }
}
