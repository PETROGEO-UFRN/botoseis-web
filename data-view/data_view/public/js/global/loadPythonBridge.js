const DEBOUNCE_TIME_IN_MS = 500
const THROTTLE_TIME_IN_MS = 2000

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

function throttlePythonBridge() {
  let inThrottle = false

  return function (newValues) {
    if (!inThrottle) {
      inThrottle = true
      loadPythonBridge(newValues)

      setTimeout(() => {
        console.log("triggered setTimeout")
        inThrottle = false
      }, THROTTLE_TIME_IN_MS)
    }
  }
}
// *** set function to window making it available on bokeh js callback declared on server-side, running on client-side
window.throttlePythonBridge = throttlePythonBridge

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

  stopLoadingWhenUnchanged(
    update_plot_options_trigger.data,
    newValuesWrapped
  )
  update_plot_options_trigger.data = { ...newValuesWrapped }
}

function stopLoadingWhenUnchanged(oldDataArray, newDataArray) {
  const keysToStop = Object.entries(newDataArray).map(([key]) => {
    if (!(key in oldDataArray))
      return
    // *** data needs to be compared as string to avoid memory address comparison
    const isDataUnchanged = oldDataArray[key].toString() === newDataArray[key].toString()
    if (isDataUnchanged)
      return key
    // *** filter removes undefined values
  }).filter(key => key)

  if (keysToStop.length)
    window.finishLoading(keysToStop)
}
