from typing import Callable
from bokeh.models import ColumnDataSource

from ..triggerBridgeFeedback import triggerBridgeFeedback
from ...plots.BasicPlot import Visualization


def bridgeCallbackFactory(visualization: Visualization) -> Callable:
    strategies = {
        'imageVisible': lambda value: visualization.updateImageVisibility(value[0]),
        'wiggleVisible': lambda value: visualization.updateWiggleVisibility(value[0]),
        'colormap': lambda value: visualization.updateColormap(value[0]),
        'gain': lambda value: visualization.updateGain(value[0]) if isinstance(value[0], dict) else None,
    }

    def onBridgeTrigger(feedbackBridgeModel: ColumnDataSource, attr, old, new):
        if not isinstance(new, dict):
            return
        for key, value in new.items():
            if key in strategies:
                strategies[key](value)
                triggerBridgeFeedback(feedbackBridgeModel, key)

    return onBridgeTrigger
