let nmo_trigger = false

function applyNMO() {
  nmo_trigger = !nmo_trigger
  debouncedPythonBridge({ "apply_nmo_triger": nmo_trigger })
}