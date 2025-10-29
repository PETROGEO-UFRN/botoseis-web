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

  const gathersAmountLoadingIcon = document.querySelector("#loading-num_loadedgathers-icon")

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

    gathersAmountLoadingIcon.classList.toggle("is-loading")
    debouncedPythonBridge({ num_loadedgathers: newGathersAmount })
  })

  const updateShotGatherPositionNumber = (event) => {
    displayLoadingOnGatherSelection()
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
