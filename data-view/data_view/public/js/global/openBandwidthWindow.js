let open_bandwidth = false

function openBandwidthWindow(workflowId) {
  window.open(
    '/bandwidth?workflowId=' + workflowId,
    '_blank',
    'width=500,height=600,popup=yes'
  )

  open_bandwidth = !open_bandwidth
  debouncedPythonBridge({ open_bandwidth })
}
