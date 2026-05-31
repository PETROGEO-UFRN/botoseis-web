window.semblancePlotHoverCallback = ({
  index_in_plot_pair,
  hasPicks,
  geometry,
  nativeCrosshair,
}) => {
  renderCrosshair({ geometry, nativeCrosshair })
  renderNMOCurve({ geometry, index_in_plot_pair, hasPicks })
}

function renderCrosshair({ geometry, nativeCrosshair }) {
  if (!nativeCrosshair.active)
    return

  const hLine = document.getElementById('crosshair-horizontal-line')
  if (geometry.x == Infinity || geometry.y == Infinity)
    return hLine.style.display = "none"

  hLine.style.display = "block"
  hLine.style.transform = `translate3d(0, ${geometry.sy}px, 0)`
}

function renderNMOCurve({ geometry, index_in_plot_pair, hasPicks }) {
  const isNMOAplied = (
    window.is_nmo_triggered && hasPicks
  )
  if (isNMOAplied)
    return

  if (geometry.x == Infinity || geometry.y == Infinity) {
    const semblance_plot_hover = {
      index_in_plot_pair,
      x: null,
      y: null,
    }
    return window.loadPythonBridge({
      semblance_plot_hover
    })
  }

  const semblance_plot_hover = {
    index_in_plot_pair,
    x: geometry.x,
    y: geometry.y,
  }

  window.throttlePythonBridge({ semblance_plot_hover })
}
