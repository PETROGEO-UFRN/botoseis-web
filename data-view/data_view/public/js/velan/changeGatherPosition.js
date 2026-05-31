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
  // *** adding number_of_gathers_per_time twice
  // *** considering 2 gathers are rendered per time
  const secondDisplayedGatherOnNewPosition = (
    newPosition +
    number_of_gathers_per_time
  )
  if (secondDisplayedGatherOnNewPosition > shotGatherPositionNumber.max)
    return

  displayLoadingOnGatherSelection()
  shotGatherPositionNumber.value = newPosition
  debouncedPythonBridge({ gather_index_start: newPosition - 1 })
}
