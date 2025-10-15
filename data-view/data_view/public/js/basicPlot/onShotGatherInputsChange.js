document.addEventListener("DOMContentLoaded", () => {
  const gathersAmountInput = document.querySelector(
    '#gathers-amount-input'
  )
  const shotGatherPositionNumber = document.querySelector(
    '#shot-gather-position-number'
  )
  const shotGatherPositionSlider = document.querySelector(
    '#shot-gather-position-slider'
  )

  // *** stop when there is no such input
  // *** tipcaly when the input has no shot gather
  if (!gathersAmountInput) return

  gathersAmountInput.addEventListener('change', (event) => {
    const newGathersAmount = event.target.value

    if (newGathersAmount > 1) {
      newPositionLimit = shotGatherPositionNumber.max - (newGathersAmount - 1)
      shotGatherPositionNumber.max = newPositionLimit
      shotGatherPositionSlider.max = newPositionLimit
    }

    debouncedPythonBridge({ num_loadedgathers: newGathersAmount })
  })

  const updateShotGatherPositionNumber = (event) => {
    const newPosition = event.target.value
    shotGatherPositionNumber.value = newPosition
    shotGatherPositionSlider.value = newPosition
    // *** server uses 0 based index
    debouncedPythonBridge({ gather_index_start: newPosition - 1 })
  }

  shotGatherPositionNumber.addEventListener(
    'change',
    updateShotGatherPositionNumber
  )
  shotGatherPositionSlider.addEventListener(
    'change',
    updateShotGatherPositionNumber
  )
})
