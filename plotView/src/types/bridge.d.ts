interface IBridgeValidActions {
  ping?: boolean
  gatherIndex?: number
}

interface IEmptyApiResponse {
  ok: boolean
}

type PackedBridgeValidActionsType = {
  [K in keyof IBridgeValidActions]: [IBridgeValidActions[K]]
}

type plotSetupPropsType = Record<string, unknown>
