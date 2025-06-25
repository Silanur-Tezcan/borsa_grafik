# BIST Hisse Senedi Grafik Görselleştirme Uygulaması

Bu proje, Python dilinde geliştirilmiş ve `yfinance`, `pandas`, `numpy`, `matplotlib` gibi kütüphaneler kullanılarak Borsa İstanbul (BIST) verileri üzerinden belirli bir hisse senedinin grafiksel analizini yapmayı amaçlamaktadır.

## 🚀 Özellikler
- BIST'te işlem gören herhangi bir hissenin verilerini otomatik olarak çekme
- Seçilen tarih aralığına göre veri analizi
- Kapanış fiyatlarına göre çizilen zaman serisi grafik
- Verinin pandas DataFrame olarak işlenmesi ve görselleştirilmesi
- Kullanıcıdan hisse kodu ve tarih girişi alma (isteğe bağlı yapılandırılabilir)

## 🧰 Kullanılan Kütüphaneler
- `yfinance`
- `pandas`
- `numpy`
- `matplotlib`
- (Opsiyonel: `seaborn`, `plotly` gibi görselleştirme araçları)

## 🔧 Kurulum

Gerekli kütüphaneleri yüklemek için terminalde aşağıdaki komutu çalıştırabilirsiniz:

```bash
pip install yfinance pandas numpy matplotlib
