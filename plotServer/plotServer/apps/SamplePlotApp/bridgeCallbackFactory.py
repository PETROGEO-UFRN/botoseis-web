from typing import Callable
from bokeh.models import ColumnDataSource
from ..triggerBridgeFeedback import triggerBridgeFeedback
from .SamplePlot import SamplePlot


def bridgeCallbackFactory(plot: SamplePlot):
    def handlePing(_value):
        plot.handle_ping()

    callbackStrategies: dict[str, Callable] = {'ping': handlePing}

    def onBridgeTrigger(feedbackBridgeModel: ColumnDataSource, attr, old, new):
        if not isinstance(new, dict):
            return
        for key, value in new.items():
            if key in callbackStrategies:
                callbackStrategies[key](value)
                triggerBridgeFeedback(feedbackBridgeModel, key)
    return onBridgeTrigger
