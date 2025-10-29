const applyGain = () => {
  const loadingIcon = document.querySelector("#loading-wagc-icon")
  loadingIcon.classList.toggle("is-loading")

  const gainNumberInput = document.querySelector("#gain-control-window-input");
  const gainValue = gainNumberInput.value

  const selectedGainTypeRadio = document.querySelector('input[name="gain-type-radio"]:checked');
  const selectedGainType = selectedGainTypeRadio.value

  debouncedPythonBridge({
    wagc: gainValue,
    gain_option: selectedGainType
  })
}
