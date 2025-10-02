document.addEventListener("DOMContentLoaded", () => {
  const imageCheckbox = document.querySelector("#image-switch");
  imageCheckbox.addEventListener("change", (event) => {
    imageCheckbox.checked = event.target.checked;

    loadPythonBridge({ toggle_image: event.target.checked });
  });

  const wiggleCheckbox = document.querySelector("#wiggle-switch");
  wiggleCheckbox.addEventListener("change", (event) => {
    wiggleCheckbox.checked = event.target.checked;

    loadPythonBridge({ toggle_wiggle: event.target.checked });
  });

  const areasCheckbox = document.querySelector("#areas-switch");
  areasCheckbox.addEventListener("change", (event) => {
    areasCheckbox.checked = event.target.checked;

    loadPythonBridge({ toggle_areas: event.target.checked });
  });

  const gainControlWindowInput = document.querySelector("#gain-control-window-input");
  gainControlWindowInput.addEventListener("change", (event) => {
    const value = event.target.value
    loadPythonBridge({ wagc: value })
  })

  const percentileClipInput = document.querySelector("#percentile-clip-input");
  percentileClipInput.addEventListener("change", (event) => {
    const value = event.target.value

    if (value <= 0)
      return percentileClipInput.value = 0
    if (value > 100)
      return percentileClipInput.value = 0

    loadPythonBridge({ percentile_clip: value })
  })

  const gainRadios = document.querySelectorAll('input[name="gain-type-radio"]');
  gainRadios.forEach(radio => {
    radio.addEventListener('change', (event) => {
      loadPythonBridge({ gain_option: event.target.value });
    });
  });
})
