from . import MultiGatherVisualization, StackVisualization


# *** Adapter: [MultiGatherVisualization, StackVisualization]

def visualization_factory(filename: str, gather_key: str | None = None):
    if gather_key:
        return MultiGatherVisualization(filename, gather_key)
    return StackVisualization(filename)
