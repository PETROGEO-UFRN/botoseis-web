window.semblancePlotHoverCallback = ({
  index_in_plot_pair,
  hasPicks,
  geometry,
}) => {
  renderNMOCurve({ geometry, index_in_plot_pair, hasPicks })
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
