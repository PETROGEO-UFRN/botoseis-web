import { plotAPI } from '@/config/plotApiConfig'
import type { PLOT_TYPES_ENUM } from '@/constants/PLOT_TYPES'

interface IGetPlotScriptProps {
  plotType: PLOT_TYPES_ENUM
  workflowId: string
  origin?: OriginType
  setupProps?: plotSetupPropsType
}

interface IGetPlotScriptResult {
  ok: boolean
  scriptTagAsString?: string
}

export async function getPlotScript({
  plotType,
  workflowId,
  origin,
  setupProps
}: IGetPlotScriptProps): Promise<IGetPlotScriptResult> {
  try {
    let queryParams = `workflowId=${workflowId}`
    if (origin) {
      queryParams += `&origin=${encodeURIComponent(origin)}`
    }
    if (setupProps) {
      const setup = btoa(JSON.stringify(setupProps))
      queryParams += `&setup=${encodeURIComponent(setup)}`
    }
    const routePath = `${plotAPI.baseURL}${plotAPI.path}/${plotType}`
    const routeURL = `${routePath}?${queryParams}`

    console.log(`Fetching plot script from: ${routeURL}`)
    console.log(routeURL)
    const response = await fetch(routeURL)

    if (!response.ok) return { ok: false }

    const data = await response.json()
    return { ok: true, scriptTagAsString: data.script }
  } catch (error) {
    console.error(error)
    return { ok: false }
  }
}
