from typing import Literal
from seismicio.Models.SuDataModel import SuFile
import numpy as np
from bokeh.plotting import figure
from bokeh.models import LogColorMapper
from bokeh.layouts import row

from ..BaseVisualization import BaseVisualization
from ..BaseVisualization import BasePlotOptionsState


class Visualization(BaseVisualization):
    sufile: SuFile
    plots_row: row
    plots: dict[
        Literal["input", "heat", "image"],
        figure
    ]

    def __init__(
        self,
        filename: str,
        plot_options_state: BasePlotOptionsState,
        gather_key: str | None = None,
    ) -> None:
        self.plots = dict()
        super().__init__(
            filename,
            plot_options_state,
            gather_key,
        )

        data = self.getBaseData()
        self.__create_mock_plots(data)

    def __create_mock_plots(self, data):
        self.plots["input"] = figure(
            title="Mock source",
            sizing_mode="stretch_both",
        )
        self.plots["input"].line(
            x=data.flatten(),
            y=data.flatten(),
            line_width=2,
        )

        self.plots["heat"] = figure(
            title="Mock",
            sizing_mode="stretch_both",
        )
        color_mapper = LogColorMapper(palette="Viridis256", low=1, high=1e7)
        self.plots["heat"].image(
            image=[data],
            color_mapper=color_mapper,
            dh=1.0,
            dw=1.0,
            x=0,
            y=0
        )

        self.plots["image"] = figure(
            title="Mock",
            sizing_mode="stretch_both",
            x_range=(0, 1),
            y_range=(0, 1),
        )
        self.plots["image"].image(
            image=[data],
            x=0,
            y=0,
            dw=1.0,
            dh=1.0,
        )
        self.plots_row = row(
            self.plots["input"],
            self.plots["heat"],
            self.plots["image"],
            sizing_mode='stretch_both',
        )

    def handle_state_change(self):
        pass
