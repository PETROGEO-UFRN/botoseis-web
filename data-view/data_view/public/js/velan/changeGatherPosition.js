function previusGatherPostion() {
  const shotGatherPositionNumber = document.querySelector(
    '#shot-gather-position-number'
  )

  const newPosition = parseInt(shotGatherPositionNumber.value) - number_of_gathers_per_time
  if (newPosition < first_cdp)
    return

  displayLoadingOnGatherSelection()
  shotGatherPositionNumber.value = newPosition

  debouncedPythonBridge({ gather_index_start: newPosition - 1 })
}

function nextGatherPostion() {
  const shotGatherPositionNumber = document.querySelector(
    '#shot-gather-position-number'
  )

  const newPosition = parseInt(shotGatherPositionNumber.value) + number_of_gathers_per_time
  if (newPosition > shotGatherPositionNumber.max)
    return

  displayLoadingOnGatherSelection()
  shotGatherPositionNumber.value = newPosition
  debouncedPythonBridge({ gather_index_start: newPosition - 1 })
}
