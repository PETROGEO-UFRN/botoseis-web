let picks_trigger = false

function savePicks() {
  picks_trigger = !picks_trigger
  console.log({ picks_trigger })
  debouncedPythonBridge({ save_picks_triger: picks_trigger })
}