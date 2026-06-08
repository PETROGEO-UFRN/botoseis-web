from functools import partial
from typing import Callable
from bokeh.document import Document
from bokeh.models import ColumnDataSource

from ..constants.BOKEH_REACT_BRIDGE import (
    BRIDGE_MODEL_NAME,
    BRIDGE_FEEDBACK_MODEL_NAME,
    BRIDGE_METADATA_MODEL_NAME,
)

def bridgeModelFactory(
    document: Document,
    callback: Callable[[str, object, object], None],
    metadata: dict | None = None,
) -> ColumnDataSource:
    """
    Creates the ColumnDataSource bridge model that useBokeh targets by name.

    Creates 2 ColumnDataSource models:
    - First for receiving data from the client and triggering the callback.
    - Second for providing feedback to the client.

    When ``metadata`` is given, a third read-only model carries server-computed
    values (e.g. ``num_gathers``) the client reads once to configure itself.

    Returns the feedback model so callers can push server-initiated updates
    back to React through the already-wired channel.
    """

    bridgeModel = ColumnDataSource(data={}, name=BRIDGE_MODEL_NAME)
    feedbackBridgeModel = ColumnDataSource(data={}, name=BRIDGE_FEEDBACK_MODEL_NAME)

    boundCallback = partial(callback, feedbackBridgeModel)
    bridgeModel.on_change('data', boundCallback)

    document.add_root(bridgeModel)
    document.add_root(feedbackBridgeModel)

    if metadata is not None:
        metadataModel = ColumnDataSource(
            data={key: [value] for key, value in metadata.items()},
            name=BRIDGE_METADATA_MODEL_NAME,
        )
        document.add_root(metadataModel)

    return feedbackBridgeModel
