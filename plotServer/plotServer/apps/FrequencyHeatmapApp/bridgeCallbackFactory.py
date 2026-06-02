from typing import Callable
from bokeh.models import ColumnDataSource

from ..triggerBridgeFeedback import triggerBridgeFeedback


def bridgeCallbackFactory() -> Callable:
    """Read-only module: no bridge actions yet. Empty strategies keep
    the loader's bridge-model lookup happy."""
    strategies = {}

    def onBridgeTrigger(feedbackBridgeModel: ColumnDataSource, attr, old, new):
        if not isinstance(new, dict):
            return
        for key, value in new.items():
            if key in strategies:
                strategies[key](value)
                triggerBridgeFeedback(feedbackBridgeModel, key)

    return onBridgeTrigger
