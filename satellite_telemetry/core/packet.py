from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TelemetryPacket:
    satellite_id: str  # "SAT-1" veya "SAT-2"
    packet_type: str  # "telemetry", "power", "termal"
    timestamp: float
    values: dict[str, float]

