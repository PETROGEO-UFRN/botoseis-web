document.addEventListener("DOMContentLoaded", () => {
  const imageCheckbox = document.querySelector("#image-switch");
  imageCheckbox.addEventListener("change", (event) => {
    imageCheckbox.checked = event.target.checked;

    debouncedPythonBridge({ toggle_image: event.target.checked });
  });

  const wiggleCheckbox = document.querySelector("#wiggle-switch");
  wiggleCheckbox.addEventListener("change", (event) => {
    wiggleCheckbox.checked = event.target.checked;

    debouncedPythonBridge({ toggle_wiggle: event.target.checked });
  });

  const colormapInput = document.querySelector("#colormap-input")
  colormapInput.addEventListener("change", (event) => {
    const value = event.target.value
    colormapInput.value = value

    debouncedPythonBridge({ palette: value })
  })

  const colormapLabelButton = document.querySelector(".colormap-label .label-button")
  colormapLabelButton.addEventListener("click", () => {
    colormapInput.showPicker()
  })

  const gainControlWindowInput = document.querySelector("#gain-control-window-input");
  gainControlWindowInput.addEventListener("change", (event) => {
    const value = event.target.value

    if (value <= 0)
      return gainControlWindowInput.value = 0
  })
})
