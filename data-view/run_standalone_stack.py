from os import getenv, getcwd
from data_view.core import visualization_factory
from bokeh.plotting import curdoc

SU_FILE_PATH = getenv(
    'SAMPLE_SU_FILE_PATH',
    f'{getcwd()}/../server/app/tests/mock_seismic_data/marmousi_4ms_stack.su'
)
main = visualization_factory(
    filename=SU_FILE_PATH
)

curdoc().add_root(main.root_layout)
