from __future__ import annotations

from queue import Empty, Full, Queue

from core.packet import TelemetryPacket


class PacketIngestionService:

    def __init__(self, maxsize: int = 1000) -> None:
        self._queue: Queue[TelemetryPacket] = Queue(maxsize=maxsize)

    def ingest(self, packet: TelemetryPacket) -> bool:
        try:
            self._queue.put_nowait(packet)
            return True
        except Full:
            return False

    def drain(self) -> list[TelemetryPacket]:
        drained: list[TelemetryPacket] = []
        while True:
            try:
                drained.append(self._queue.get_nowait())
            except Empty:
                return drained

