function applyNMO() {
  window.is_nmo_triggered = !window.is_nmo_triggered
  debouncedPythonBridge({ "nmo_trigger": window.is_nmo_triggered })

  const NMOOperationButton = document.querySelector("#apply-nmo")
  if (window.is_nmo_triggered)
    NMOOperationButton.textContent = "REMOVE NMO"
  else
    NMOOperationButton.textContent = "APPLY NMO"
}
