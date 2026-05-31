from bokeh.models import ColumnDataSource


def triggerBridgeFeedback(feedbackBridgeModel: ColumnDataSource, key: str):
    newData = dict(feedbackBridgeModel.data)
    newData[key] = [not newData.get(key, [False])[0]]
    feedbackBridgeModel.data = newData
