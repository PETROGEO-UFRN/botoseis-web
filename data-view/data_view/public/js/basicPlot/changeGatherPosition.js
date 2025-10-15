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

  shotGatherPositionNumber.value = newPosition
  shotGatherPositionSlider.value = newPosition
  loadPythonBridge({ gather_index_start: newPosition - 1 })
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

  shotGatherPositionNumber.value = newPosition
  shotGatherPositionSlider.value = newPosition
  loadPythonBridge({ gather_index_start: newPosition - 1 })
}
