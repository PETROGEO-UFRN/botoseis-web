function loadPythonBridge(newValues) {
  const bokehDocument = Bokeh.documents[0]
  const update_plot_options_trigger = bokehDocument.get_model_by_name(
    "update_plot_options_trigger"
  );
  if (update_plot_options_trigger) {
    const newValuesWrapped = Object.fromEntries(
      Object.entries(newValues).map(([key, value]) => (
        [key, [value]]
      ))
    )

    update_plot_options_trigger.data = { ...newValuesWrapped }
  } else {
    console.error("trigger not found")
  }
}
