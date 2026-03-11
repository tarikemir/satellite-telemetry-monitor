from __future__ import annotations

import random
import time
from threading import Event, Thread

from core.ingestion import PacketIngestionService
from core.packet import TelemetryPacket


class PacketSimulator:

    def __init__(self, ingestion_service: PacketIngestionService) -> None:
        self._ingestion = ingestion_service
        self._stop = Event()
        self._thread = Thread(target=self._run, name="PacketSimulator", daemon=True)
        self._type_i = 0
        self._sat_i = 0

    def start(self) -> None:
        self._stop.clear()
        if not self._thread.is_alive():
            self._thread = Thread(target=self._run, name="PacketSimulator", daemon=True)
            self._thread.start()

    def stop(self) -> None:
        self._stop.set()

    def _values_for(self, packet_type: str) -> dict[str, float]:
        r = random.uniform
        if packet_type == "telemetry":
            return {
                "cpu_usage": r(20, 90),
                "cpu_temp": r(30, 70),
                "ram_usage": r(10, 80),
                "signal_strength": r(-90, -40),
            }
        if packet_type == "power":
            return {"battery_voltage": r(22, 28), "solar_current": r(0, 5), "power_consumption": r(10, 40)}
        return {"panel_temp": r(-20, 60), "heat_sink_temp": r(20, 50), "coolant_flow": r(0.5, 2.0)}

    def _run(self) -> None:
        sats = ("SAT-1", "SAT-2")
        types = ("telemetry", "power", "thermal")
        while not self._stop.is_set():
            for _ in range(random.randint(1, 3)):
                sat = sats[self._sat_i % 2]
                ptype = types[self._type_i % 3]
                self._sat_i += 1
                self._type_i += 1
                pkt = TelemetryPacket(sat, ptype, time.time(), self._values_for(ptype))
                if random.random() < 0.02:
                    time.sleep(0.5)
                if random.random() >= 0.05:
                    self._ingestion.ingest(pkt)
            time.sleep(0.1)

