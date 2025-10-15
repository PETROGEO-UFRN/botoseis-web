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

  const areasCheckbox = document.querySelector("#areas-switch");
  // *** check if there is no such input
  // *** tipcaly when the input has no shot gather
  // *** is will also have no areas-switch
  if (areasCheckbox)
    areasCheckbox.addEventListener("change", (event) => {
      areasCheckbox.checked = event.target.checked;

      debouncedPythonBridge({ toggle_areas: event.target.checked });
    });

  const colormapInput = document.querySelector("#colormap-input")
  colormapInput.addEventListener("change", (event) => {
    const value = event.target.value
    colormapInput.value = value

    debouncedPythonBridge({ palette: value })
  })

  const colormapLabel = document.querySelector(".colormap-label")
  colormapLabel.addEventListener("click", (event) => {
    colormapInput.showPicker()
  })

  const gainControlWindowInput = document.querySelector("#gain-control-window-input");
  gainControlWindowInput.addEventListener("change", (event) => {
    const value = event.target.value

    if (value <= 0)
      return gainControlWindowInput.value = 0

    debouncedPythonBridge({ wagc: value })
  })

  const percentileClipInput = document.querySelector("#percentile-clip-input");
  percentileClipInput.addEventListener("change", (event) => {
    const value = event.target.value

    debouncedPythonBridge({ percentile_clip: value })
  })

  const gainRadios = document.querySelectorAll('input[name="gain-type-radio"]');
  gainRadios.forEach(radio => {
    radio.addEventListener('change', (event) => {
      debouncedPythonBridge({ gain_option: event.target.value });
    });
  });
})
