from pathlib import Path

__TAMPLATES_FOLDER = Path(__file__).parent.parent / "templates"

BASIC_PLOT_TEMPLATE_PATH = (
    __TAMPLATES_FOLDER / "basicPlot" / "index.html"
).resolve()

VELAN_TEMPLATE_PATH = (
    __TAMPLATES_FOLDER / "velan" / "index.html"
).resolve()

VELOCITY_MODEL_TEMPLATE_PATH = (
    __TAMPLATES_FOLDER / "velocityModel" / "index.html"
).resolve()

STATIC_FILES_PATH = (Path(__file__).parent.parent / "public").resolve()
