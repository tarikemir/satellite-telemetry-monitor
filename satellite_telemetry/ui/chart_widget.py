from __future__ import annotations

import time

import pyqtgraph as pg
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from config.chart_definitions import ChartDefinition


class ChartWidget(QWidget):

    def __init__(self, definition: ChartDefinition, satellite_id: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._definition = definition
        self._satellite_id = satellite_id

        self._plot = pg.PlotWidget()
        self._plot.setTitle(definition.alias)
        self._plot.setLabel("left", definition.unit)
        self._plot.showGrid(x=True, y=True, alpha=0.25)
        self._curve = self._plot.plot(pen=pg.mkPen(color=definition.color, width=2))

        layout = QVBoxLayout()
        layout.setContentsMargins(6, 6, 6, 6)
        layout.addWidget(self._plot)
        self.setLayout(layout)

    @property
    def definition(self) -> ChartDefinition:
        return self._definition

    @property
    def satellite_id(self) -> str:
        return self._satellite_id

    def update_data(self, timestamps: list[float], values: list[float]) -> None:
        cutoff = time.time() - 60.0
        xs: list[float] = []
        ys: list[float] = []
        for t, v in zip(timestamps, values):
            if t >= cutoff:
                xs.append(t)
                ys.append(v)
        self._curve.setData(xs, ys)

