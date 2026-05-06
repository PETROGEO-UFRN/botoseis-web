interface IBridgeValidActions {
  ping?: boolean
}

interface IEmptyApiResponse {
  ok: boolean
}

type PackedBridgeValidActionsType = {
  [K in keyof IBridgeValidActions]: [IBridgeValidActions[K]]
}

type plotSetupPropsType = Record<string, unknown>
