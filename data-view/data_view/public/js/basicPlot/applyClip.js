const applyClip = () => {
  const loadingIcon = document.querySelector("#loading-percentile_clip-icon")
  loadingIcon.classList.toggle("is-loading")

  const percentileClipInput = document.querySelector("#percentile-clip-input");
  const value = percentileClipInput.value

  debouncedPythonBridge({ percentile_clip: value })
}
