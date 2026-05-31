from typing import Callable
from bokeh.models import ColumnDataSource

from ..triggerBridgeFeedback import triggerBridgeFeedback


def bridgeCallbackFactory() -> Callable:
    """
    Step 4 velocityModel is read-only; no actions are dispatched.
    The bridge model is still required so useBokehLoader recognizes the
    document as ready. Strategies remain empty until cross-plot
    remoteGatherIndex syncing lands (Step 5+).
    """
    strategies = {}

    def onBridgeTrigger(feedbackBridgeModel: ColumnDataSource, attr, old, new):
        if not isinstance(new, dict):
            return
        for key, value in new.items():
            if key in strategies:
                strategies[key](value)
                triggerBridgeFeedback(feedbackBridgeModel, key)

    return onBridgeTrigger
