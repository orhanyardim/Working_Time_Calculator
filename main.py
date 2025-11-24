import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

# --- YAPILANDIRMA ---
DATA_FILE = "veriler.json"
TIME_FORMAT = "%H:%M"

def load_data() -> List[Dict]:
    """
    JSON dosyasındaki mevcut kayıtları okur.
    Dosya yoksa boş bir liste döndürür.
    """
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, ValueError):
        return []

def save_data(data: List[Dict]):
    """
    Verilen listeyi JSON formatında dosyaya kaydeder.
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def input_time(prompt: str) -> datetime:
    """Kullanıcıdan saat bilgisi alır ve datetime objesi döndürür."""
    while True:
        time_str = input(prompt).strip()
        try:
            return datetime.strptime(time_str, TIME_FORMAT)
        except ValueError:
            print("Hatalı format! Lütfen 'HH:MM' formatında giriniz (ör: 14:30).")

def calculate_duration(start_dt: datetime, end_dt: datetime) -> float:
    """
    İki saat arasındaki farkı dakika cinsinden hesaplar.
    Eğer bitiş saati başlangıçtan küçükse (gece yarısı geçişi), bitişe 1 gün ekler.
    """
    if end_dt < start_dt:
        # Örnek: Başlangıç 23:00, Bitiş 01:00. Bitişe 1 gün ekle.
        end_dt += timedelta(days=1)
    
    diff = end_dt - start_dt
    return diff.total_seconds() / 60

def print_summary(data: List[Dict]):
    """Mevcut verilerin özet tablosunu ve toplam süreyi yazdırır."""
    if not data:
        print("\nHenüz kaydedilmiş bir veri yok.")
        return

    print(f"\n{'Tarih':<12} {'Başlangıç':<10} {'Bitiş':<10} {'Süre (dk)':<10} {'Süre (saat)':<12}")
    print("-" * 55)

    total_minutes = 0
    
    for entry in data:
        # JSON'dan gelen string verileri ekrana bas
        print(f"{entry['date']:<12} {entry['start']:<10} {entry['end']:<10} {entry['minutes']:<10} {entry['hours']:<12}")
        total_minutes += entry['minutes']

    total_hours = total_minutes / 60
    print("-" * 55)
    print(f"GENEL TOPLAM: {total_minutes} dakika ({total_hours:.2f} saat)\n")

def main():
    # 1. Mevcut veriyi yükle
    history = load_data()
    
    # 2. Önceki kayıtları göster
    print("--- MEVCUT KAYITLAR ---")
    print_summary(history)

    # 3. Yeni Giriş
    while True:
        choice = input("Yeni zaman aralığı eklemek ister misiniz? (e/h): ").lower().strip()
        if choice != 'e':
            break

        print("\n--- Yeni Kayıt ---")
        start_dt = input_time("Giriş saati (HH:MM): ")
        end_dt = input_time("Çıkış saati (HH:MM): ")
        
        minutes = calculate_duration(start_dt, end_dt)
        hours = round(minutes / 60, 2)
        
        # Bugünün tarihini al (Kayıt tarihi olarak)
        today_str = datetime.now().strftime("%Y-%m-%d")

        # Yeni kaydı oluştur
        new_entry = {
            "date": today_str,
            "start": start_dt.strftime(TIME_FORMAT),
            "end": end_dt.strftime(TIME_FORMAT),
            "minutes": round(minutes),
            "hours": hours
        }
        
        # Listeye ekle ve kaydet
        history.append(new_entry)
        save_data(history)
        print(">> Kayıt başarıyla eklendi!")

    # 4. Çıkışta son durumu göster
    print_summary(history)

if __name__ == "__main__":
    main()