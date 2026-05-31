from typing import Callable
from bokeh.models import ColumnDataSource

from ..triggerBridgeFeedback import triggerBridgeFeedback
from ...plots.Velan import Visualization
from ...services.RestAPIConsumer import RestAPIConsumer


def bridgeCallbackFactory(
    visualization: Visualization,
    consumer: RestAPIConsumer,
) -> Callable:
    strategies = {
        'gatherIndex': lambda value: visualization.updateGatherIndex(value[0]),
        'applyNMO': lambda value: visualization.apply_nmo() if value[0] else visualization.remove_nmo(),
        'reusePicks': lambda _: visualization.reuse_picks(),
        'savePicks': lambda _: consumer.save_picks(visualization.picking_data),
        'isNMOHyperboleOn': lambda value: visualization.update_nmo_hyperbole_state(value[0]),
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
