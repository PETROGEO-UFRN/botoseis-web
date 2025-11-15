let trigger = false

function applyNMO() {
  trigger = !trigger
  debouncedPythonBridge({ "apply_nmo_triger": trigger })
}