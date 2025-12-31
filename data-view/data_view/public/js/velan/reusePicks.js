let reuse_picks_trigger = false

function reusePicks() {
  reuse_picks_trigger = !reuse_picks_trigger
  debouncedPythonBridge({ reuse_picks: reuse_picks_trigger })
}
