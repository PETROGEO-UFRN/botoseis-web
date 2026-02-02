let open_bandwidth = false

function openBandwidthWindow(workflowId) {
  window.open(
    '/bandwidth?workflowId=' + workflowId,
    '_blank',
    'width=768,height=384,popup=yes'
  )

  open_bandwidth = !open_bandwidth
  debouncedPythonBridge({ open_bandwidth })
}

function openFrequencyHeatmapWindow(workflowId) {
  window.open(
    '/frequency-heatmap?workflowId=' + workflowId,
    '_blank',
    'width=768,height=384,popup=yes'
  )

  open_bandwidth = !open_bandwidth
  debouncedPythonBridge({ open_bandwidth })
}
