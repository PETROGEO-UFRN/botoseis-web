from types import SimpleNamespace


from .num_loadedgathers_spinner import create_num_loadedgathers_spinner
from .seismic_visualization import create_seismic_plot_wrapper
from .gather_index_start_slider import create_gather_index_start_slider
from .gather_value_label import GatherValueWrapper
from .percentile_clip_input import create_percentile_clip_input
from .wagc_input import create_wagc_input
from .gain_option_picker import create_gain_option_picker


widgets = SimpleNamespace(
    create_num_loadedgathers_spinner=create_num_loadedgathers_spinner,
    create_seismic_plot_wrapper=create_seismic_plot_wrapper,
    create_gather_index_start_slider=create_gather_index_start_slider,
    GatherValueWrapper=GatherValueWrapper,
    create_percentile_clip_input=create_percentile_clip_input,
    create_wagc_input=create_wagc_input,
    create_gain_option_picker=create_gain_option_picker
)
