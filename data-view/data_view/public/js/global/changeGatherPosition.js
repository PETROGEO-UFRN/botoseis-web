function previusGatherPostion() {
  const shotGatherPositionNumber = document.querySelector(
    '#shot-gather-position-number'
  )
  const shotGatherPositionSlider = document.querySelector(
    '#shot-gather-position-slider'
  )

  const newPosition = parseInt(shotGatherPositionNumber.value) - 1
  if (newPosition < 1)
    return

  displayLoadingOnGatherSelection()
  shotGatherPositionNumber.value = newPosition
  if (shotGatherPositionSlider)
    shotGatherPositionSlider.value = newPosition
  debouncedPythonBridge({ gather_index_start: newPosition - 1 })
}

function nextGatherPostion() {
  const shotGatherPositionNumber = document.querySelector(
    '#shot-gather-position-number'
  )
  const shotGatherPositionSlider = document.querySelector(
    '#shot-gather-position-slider'
  )

  const newPosition = parseInt(shotGatherPositionNumber.value) + 1
  if (newPosition > shotGatherPositionNumber.max)
    return

  displayLoadingOnGatherSelection()
  shotGatherPositionNumber.value = newPosition
  if (shotGatherPositionSlider)
    shotGatherPositionSlider.value = newPosition
  debouncedPythonBridge({ gather_index_start: newPosition - 1 })
}
