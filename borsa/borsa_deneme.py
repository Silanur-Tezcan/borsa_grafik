import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from ta.trend import SMAIndicator
from prophet import Prophet  # Prophet modeli için gerekli kütüphane
import numpy as np

# Kullanıcıdan hisse senedi sembolünü al
stock_symbol = input("Hisse senedi sembolünü girin (örneğin: THYAO.IS): ").strip().upper()

try:
    # Hisse senedi verisini al (Son 1 yılın verisi)
    stock_data = yf.Ticker(stock_symbol)
    hist = stock_data.history(period="1y")  # Son 1 yılın verileri
    
    if hist.empty:
        print(f"Hata: {stock_symbol} sembolü için veri bulunamadı. Sembolün geçerli olduğundan emin olun.")
    else:
        # Verileri göster
        print(hist.head())  # İlk birkaç satırı göster
        print(f"\n{stock_symbol} hissesine ait veri başarıyla çekildi.")
        
        # Tarihi sıfırlama ve zaman dilimini kaldırma (Prophet uyumlu hale getirme)
        hist.reset_index(inplace=True)
        hist['Date'] = hist['Date'].dt.tz_localize(None)  # Zaman dilimini kaldırma
        
        # Teknik analiz için hareketli ortalamaları hesapla (20 ve 50 günlük)
        hist['MA20'] = SMAIndicator(close=hist['Close'], window=20).sma_indicator()
        hist['MA50'] = SMAIndicator(close=hist['Close'], window=50).sma_indicator()
        
        # Hareketli Ortalama Grafiği
        plt.figure(figsize=(12, 6))
        plt.plot(hist['Date'], hist['Close'], label='Kapanış Fiyatı', color='blue')
        plt.plot(hist['Date'], hist['MA20'], label='20 Günlük MA', linestyle='--', color='orange')
        plt.plot(hist['Date'], hist['MA50'], label='50 Günlük MA', linestyle='--', color='green')
        plt.title(f'{stock_symbol} Son 1 Yıl Fiyat Grafiği ve Hareketli Ortalamalar')
        plt.xlabel('Tarih')
        plt.ylabel('Kapanış Fiyatı')
        plt.legend()
        plt.grid()
        plt.show()
        
        # Prophet ile zaman serisi tahmini
        df_prophet = hist[['Date', 'Close']].rename(columns={'Date': 'ds', 'Close': 'y'})  # Prophet formatına uygun hale getirme

        # Prophet modeli oluşturma ve eğitme
        model = Prophet()
        model.add_country_holidays(country_name='TR')  # Türkiye resmi tatilleri eklenebilir (isteğe bağlı)
        model.fit(df_prophet)

        # Gelecek 7 iş günü için tahmin yapma
        future = model.make_future_dataframe(periods=7, freq='B')  # 'B' iş günlerini (hafta içi) içerir
        forecast = model.predict(future)

        # Gelecek 7 günü filtreleme
        future_days = forecast.tail(7)  # Sadece gelecek 7 iş günü
        future_dates = future_days['ds']
        future_predictions = future_days['yhat']
        future_lower = future_days['yhat_lower']
        future_upper = future_days['yhat_upper']

        # Tahmin Grafiği (Gelecek 7 İş Günü)
        plt.figure(figsize=(12, 6))
        plt.plot(future_dates, future_predictions, label='Tahmini Fiyat', color='red')
        plt.fill_between(future_dates, future_lower, future_upper, color='pink', alpha=0.2, label='Tahmin Güven Aralığı')
        plt.title(f'{stock_symbol} Tahmini (Gelecek 7 İş Günü)')
        plt.xlabel('Tarih')
        plt.ylabel('Kapanış Fiyatı')
        plt.legend()
        plt.grid()
        plt.show()

        # Tahmin Tablosu (Terminal Çıktısı)
        print("Gelecek 7 iş gününün en yüksek tahmini kapanış fiyatları:")
        print(future_days[['ds', 'yhat_upper']])
        
except Exception as e:
    print(f"Hata: Veri çekilirken bir sorun oluştu: {e}")