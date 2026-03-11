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
<img width="1395" height="923" alt="image" src="https://github.com/user-attachments/assets/fa730d21-9334-4867-9571-2277868563f0" />

<img width="1388" height="921" alt="image" src="https://github.com/user-attachments/assets/09959615-2d2b-481b-809f-e6a2d70b4fd7" />

## Mimari (genel görünüm)

<img width="121" height="411" alt="satellite-architecture drawio" src="https://github.com/user-attachments/assets/6e3fbe5f-5197-43ec-9447-0b6e3ce69865" />


## Modüller

- **`satellite_telemetry/core/packet.py`**: `TelemetryPacket` veri modeli (atomik paket).
- **`satellite_telemetry/core/ingestion.py`**: `PacketIngestionService` (thread-safe, bounded `Queue`, non-blocking ingest/drain).
- **`satellite_telemetry/core/processor.py`**: `PacketProcessor` (kilitli buffer sözlüğü, her metrik için `deque(maxlen=200)`).
- **`satellite_telemetry/config/chart_definitions.py`**: `ChartDefinition` + `CHART_REGISTRY` (grafik/metric tanımları).
- **`satellite_telemetry/ui/chart_widget.py`**: `ChartWidget` (PyQtGraph plot; son 60 saniyeyi çizer).
- **`satellite_telemetry/ui/main_window.py`**: `MainWindow` (sekme bazlı uydu görünümü, 200ms timer ile pipeline çalıştırır).
- **`satellite_telemetry/simulator/packet_simulator.py`**: `PacketSimulator` (SAT-1/SAT-2 için paket üretimi, gecikme/kayıp simülasyonu).
