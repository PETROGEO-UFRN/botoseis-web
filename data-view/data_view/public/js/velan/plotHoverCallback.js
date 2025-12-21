// *** set function o window to make it available on bokeh js callback declared on server-side, running on client-side
window.plotHoverCallback = ({ index_in_plot_pair, geometry }) => {
  if (geometry.x == Infinity || geometry.y == Infinity)
    return

  semblance_plot_hover = {
    index_in_plot_pair,
    'x': geometry.x,
    'y': geometry.y,
  };

  window.throttlePythonBridge()({ semblance_plot_hover })
}
