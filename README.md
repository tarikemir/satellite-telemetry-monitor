# satellite-telemetry-monitor

Tamamen lokal çalışan, PyQt6 + PyQtGraph tabanlı gerçek zamanlı uydu telemetrisi izleme masaüstü uygulaması. veri simülatör üzerinden üretilir ve uygulama içinde işlenip görselleştirilir.

## Kurulum

```bash
pip install -r satellite_telemetry/requirements.txt
```

## Çalıştırma

```bash
cd satellite_telemetry
python main.py
```
## Ekran Görüntüleri

<img width="1399" height="936" alt="image" src="https://github.com/user-attachments/assets/f2595384-f1c7-42eb-aef5-90e9a6ebf41e" />

<img width="1397" height="926" alt="image" src="https://github.com/user-attachments/assets/3c62d673-011e-431e-9385-f7265c7d8058" />

## Mimari (genel görünüm)

<img width="121" height="411" alt="satellite-architecture drawio" src="https://github.com/user-attachments/assets/12574d6d-11aa-438a-829b-98c9a1e61251" />


## Modüller

- **`satellite_telemetry/core/packet.py`**: `TelemetryPacket` veri modeli (atomik paket).
- **`satellite_telemetry/core/ingestion.py`**: `PacketIngestionService` (thread-safe, bounded `Queue`, non-blocking ingest/drain).
- **`satellite_telemetry/core/processor.py`**: `PacketProcessor` (kilitli buffer sözlüğü, her metrik için `deque(maxlen=200)`).
- **`satellite_telemetry/config/chart_definitions.py`**: `ChartDefinition` + `CHART_REGISTRY` (grafik/metric tanımları).
- **`satellite_telemetry/ui/chart_widget.py`**: `ChartWidget` (PyQtGraph plot; son 60 saniyeyi çizer).
- **`satellite_telemetry/ui/main_window.py`**: `MainWindow` (sekme bazlı uydu görünümü, 200ms timer ile pipeline çalıştırır).
- **`satellite_telemetry/simulator/packet_simulator.py`**: `PacketSimulator` (SAT-1/SAT-2 için paket üretimi, gecikme/kayıp simülasyonu).
