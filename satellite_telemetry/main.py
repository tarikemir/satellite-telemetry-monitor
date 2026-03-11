from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from core.ingestion import PacketIngestionService
from core.processor import PacketProcessor
from simulator.packet_simulator import PacketSimulator
from ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)

    ingestion_service = PacketIngestionService()
    processor = PacketProcessor()
    window = MainWindow(ingestion_service, processor)
    window.show()

    simulator = PacketSimulator(ingestion_service)
    simulator.start()
    try:
        return app.exec()
    finally:
        simulator.stop()


if __name__ == "__main__":
    raise SystemExit(main())

