from __future__ import annotations

from datetime import datetime

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QWidget,
    QTabWidget,
    QVBoxLayout,
)

from config.chart_definitions import CHART_REGISTRY
from core.ingestion import PacketIngestionService
from core.processor import PacketProcessor
from ui.chart_widget import ChartWidget


class MainWindow(QMainWindow):

    def __init__(self, ingestion_service: PacketIngestionService, processor: PacketProcessor) -> None:
        super().__init__()
        self._ingestion = ingestion_service
        self._processor = processor
        self._counts: dict[str, int] = {"SAT-1": 0, "SAT-2": 0}
        self._charts: dict[tuple[str, str], ChartWidget] = {}

        self.setWindowTitle("Uydu Telemetri İzleme Sistemi")
        self.resize(1400, 900)
        self.setStyleSheet(
            "QMainWindow{background:#1e1e1e;color:#ffffff;}"
            "QWidget{color:#ffffff;}"
            "QTabWidget::pane{border:0;}"
            "QLabel{font-size:14px;}"
        )

        root = QWidget()
        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(12, 12, 12, 12)
        root.setLayout(root_layout)
        self.setCentralWidget(root)

        top_bar = QHBoxLayout()
        self._status = QLabel()
        self._status.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        top_bar.addWidget(self._status, 1)
        root_layout.addLayout(top_bar)

        self._tabs = QTabWidget()
        root_layout.addWidget(self._tabs, 1)
        for sat in ("SAT-1", "SAT-2"):
            self._tabs.addTab(self._build_satellite_tab(sat), sat)

        self._timer = QTimer(self)
        self._timer.setInterval(200)
        self._timer.timeout.connect(self._on_timer)
        self._timer.start()
        self._update_status()

    def _build_satellite_tab(self, satellite_id: str) -> QWidget:
        tab = QWidget()
        grid = QGridLayout()
        grid.setContentsMargins(6, 6, 6, 6)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(10)
        tab.setLayout(grid)

        for i, definition in enumerate(CHART_REGISTRY):
            widget = ChartWidget(definition, satellite_id)
            self._charts[(satellite_id, definition.value_name)] = widget
            grid.addWidget(widget, i // 3, i % 3)
        return tab

    def _update_status(self) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        self._status.setText(f"SAT-1: {self._counts['SAT-1']} paket | SAT-2: {self._counts['SAT-2']} paket | Son güncelleme: {ts}")

    def _on_timer(self) -> None:
        packets = self._ingestion.drain()
        if packets:
            for p in packets:
                if p.satellite_id in self._counts:
                    self._counts[p.satellite_id] += 1
            self._processor.process_batch(packets)

        for sat in ("SAT-1", "SAT-2"):
            for definition in CHART_REGISTRY:
                chart = self._charts[(sat, definition.value_name)]
                xs, ys = self._processor.get_series(sat, definition.value_name)
                chart.update_data(xs, ys)
        self._update_status()

