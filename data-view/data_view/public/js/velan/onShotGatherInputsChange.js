document.addEventListener("DOMContentLoaded", () => {
  const shotGatherPositionNumber = document.querySelector(
    '#shot-gather-position-number'
  )
  const defaultValue = shotGatherPositionNumber.defaultValue

  const updateShotGatherPositionNumber = (event) => {
    let newPosition = event.target.value
    if (newPosition < defaultValue) {
      shotGatherPositionNumber.value = defaultValue
      debouncedPythonBridge({ gather_index_start: defaultValue - 1 })
      return
    }
    displayLoadingOnGatherSelection()
    const positionRest = newPosition % number_of_gathers_per_time
    if (positionRest)
      newPosition = newPosition - positionRest
    shotGatherPositionNumber.value = newPosition
    // *** server uses 0 based index
    debouncedPythonBridge({ gather_index_start: newPosition - 1 })
  }

  shotGatherPositionNumber.addEventListener(
    'change',
    updateShotGatherPositionNumber
  )
})
