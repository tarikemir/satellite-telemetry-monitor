# Teknik Rapor

## 1. Proje amacı
Bu proje, iki uydudan (SAT-1/SAT-2) gelen telemetri verisini local ortamda simüle ederek, veriyi gerçek zamanlı işleyip PyQtGraph ile görselleştiren bir masaüstü izleme uygulaması geliştirmeyi hedefler.

## 2. Mimari kararlar ve gerekçeler
- **Katmanlı yapı** (Simulation/Ingestion/Processing/UI): Sorumlulukların ayrılması ve test edilebilirlik için.
- **Pull tabanlı UI güncelleme**: UI, `QTimer(200ms)` ile veriyi “drain” eder; bloklamayı ve karmaşık sinyal/slot köprülerini azaltır.
- **Atomik paket modeli**: `TelemetryPacket` tüm alanlarıyla birlikte işlenir; kısmi güncelleme yapılmaz.

## 3. Thread güvenliği nasıl sağlandı
- Simülasyon **daemon thread**’de çalışır, Qt objeleriyle etkileşmez.
- `PacketIngestionService` yalnızca `queue.Queue` kullanır; `put_nowait/get_nowait` ile thread-safe ve non-blocking akış sağlar.
- `PacketProcessor` iç durumunu tek bir `Lock` ile korur; seri okuma/yazma yarışlarını engeller.

## 4. Bellek yönetimi
- **Bounded queue**: `Queue(maxsize=1000)` ile kuyruk büyümesi sınırlandı; doluysa paket “drop” edilebilir.
- **Rolling buffer**: Her (satellite, metric) için `deque(maxlen=200)` kullanılarak zaman serileri sabit üst sınırda tutulur.
- Grafikler yalnızca **son 60 saniyeyi** çizer; gereksiz çizim yükü azaltılır.

## 5. Karşılaşılan zorluklar
- Çalıştırma bağlamına bağlı **import** düzeni (paket/klasör) ve farklı Python sürümlerinde küçük uyumsuzluklar.
- Gerçek zamanlı çizimde performans: çok sık güncelleme UI’ı yorabilir; bu nedenle timer ile sınırlı yenileme kullanıldı.

## 6. Geliştirme önerileri
- Gerçek telemetri kaynağı (UDP/TCP/serial) için ayrı bir ingestion adaptörü.
- Metrik başına örnekleme/decimation ve çizim optimizasyonları.
- Kayıt/geri oynatma (CSV/Parquet) ve alarm/eşik tanımları.

