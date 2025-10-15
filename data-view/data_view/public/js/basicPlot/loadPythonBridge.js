const DEBOUNCE_TIME_IN_MS = 500

let bridgeDebounceTimeoutId
let debounceWaitingNewValues = {}

function debouncedPythonBridge(newValues) {
  if (bridgeDebounceTimeoutId)
    clearTimeout(bridgeDebounceTimeoutId)

  const execute = () => {
    const mergedNewValues = {
      ...newValues,
      ...debounceWaitingNewValues
    }
    debounceWaitingNewValues = mergedNewValues
    loadPythonBridge(mergedNewValues)
  }

  const hasToggleAction = Object.keys(newValues).some(key => key.includes("toggle"))

  if (hasToggleAction)
    execute()

  bridgeDebounceTimeoutId = setTimeout(() => {
    execute()
  }, DEBOUNCE_TIME_IN_MS)
}

function loadPythonBridge(newValues) {
  debounceWaitingNewValues = {}
  const bokehDocument = Bokeh.documents[0]
  const update_plot_options_trigger = bokehDocument.get_model_by_name(
    "update_plot_options_trigger"
  )
  if (!update_plot_options_trigger)
    console.error("trigger not found")

  const newValuesWrapped = Object.fromEntries(
    Object.entries(newValues).map(([key, value]) => (
      [key, [value]]
    ))
  )

  update_plot_options_trigger.data = { ...newValuesWrapped }
}
