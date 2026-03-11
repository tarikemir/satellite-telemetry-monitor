from __future__ import annotations

from collections import deque
from threading import Lock

from core.packet import TelemetryPacket

SeriesKey = tuple[str, str]  # (satellite_id, value_name)
Point = tuple[float, float]  # (timestamp, value)


class PacketProcessor:

    def __init__(self, max_points: int = 200) -> None:
        self._max_points = max_points
        self._lock = Lock()
        self._buffers: dict[SeriesKey, deque[Point]] = {}

    def process_batch(self, packets: list[TelemetryPacket]) -> None:
        with self._lock:
            for pkt in packets:
                ts = float(pkt.timestamp)
                for name, val in pkt.values.items():
                    key: SeriesKey = (pkt.satellite_id, name)
                    buf = self._buffers.get(key)
                    if buf is None:
                        buf = deque(maxlen=self._max_points)
                        self._buffers[key] = buf
                    buf.append((ts, float(val)))

    def get_series(self, satellite_id: str, value_name: str) -> tuple[list[float], list[float]]:
        key: SeriesKey = (satellite_id, value_name)
        with self._lock:
            buf = self._buffers.get(key)
            points = list(buf) if buf is not None else []
        return ([p[0] for p in points], [p[1] for p in points])

