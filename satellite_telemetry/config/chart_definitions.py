from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChartDefinition:
    packet_type: str
    value_name: str
    alias: str
    unit: str
    color: str


CHART_REGISTRY: list[ChartDefinition] = [
    ChartDefinition("telemetry", "cpu_usage", "CPU Kullanımı %", "%", "#4CAF50"),
    ChartDefinition("thermal", "cpu_temp", "CPU Sıcaklığı °C", "°C", "#FF5722"),
    ChartDefinition("power", "battery_voltage", "Batarya Voltajı V", "V", "#2196F3"),
    ChartDefinition("power", "solar_current", "Solar Akım A", "A", "#FFC107"),
    ChartDefinition("thermal", "panel_temp", "Panel Sıcaklığı °C", "°C", "#9C27B0"),
    ChartDefinition("telemetry", "signal_strength", "Sinyal Gücü dBm", "dBm", "#607D8B"),
]

