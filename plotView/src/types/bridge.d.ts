interface IBridgeValidActions {
  ping?: boolean
  gatherIndex?: number
  loadCount?: number
  imageVisible?: boolean
  wiggleVisible?: boolean
  colormap?: ColormapType
  gain?: IGainOptions
}

interface IEmptyApiResponse {
  ok: boolean
}

type PackedBridgeValidActionsType = {
  [K in keyof IBridgeValidActions]: [IBridgeValidActions[K]]
}

type plotSetupPropsType = Record<string, unknown>
