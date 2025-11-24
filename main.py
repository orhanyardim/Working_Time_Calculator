from datetime import datetime 
import os 
import re 
 
time_format = "%H:%M" 
file_name = "gorev.txt" 
 
def input_time(prompt): 
    while True: 
        time_str = input(prompt).strip() 
        try: 
            valid_time = datetime.strptime(time_str, time_format) 
            return valid_time 
        except ValueError: 
            print("Hatalı format! Lütfen saati 'HH:MM' formatında giriniz (ör: 14:30).") 
 
def input_times(): 
    times = [] 
    while True: 
        try: 
            n = int(input("Kaç adet zaman aralığı gireceksiniz? ")) 
            if n <= 0: 
                print("Lütfen pozitif bir sayı giriniz.") 
                continue 
            break 
        except ValueError: 
            print("Lütfen geçerli bir sayı giriniz.") 
 
    for i in range(n): 
        print(f"\n{i+1}. zaman aralığı:") 
        start_dt = input_time("  Giriş saati (HH:MM): ") 
        end_dt = input_time("  Çıkış saati (HH:MM): ") 
        times.append((start_dt, end_dt)) 
    return times 
 
def calculate_durations(times): 
    total_minutes = 0 
    total_hours = 0.0 
    results = [] 
 
    for start_dt, end_dt in times: 
        duration = end_dt - start_dt 
        minutes = duration.total_seconds() / 60 
        hours = minutes / 60 
        total_minutes += minutes 
        total_hours += hours 
        results.append({ 
            "Başlangıç": start_dt.strftime(time_format), 
            "Bitiş": end_dt.strftime(time_format), 
            "Süre (dk)": round(minutes), 
            "Süre (saat)": round(hours, 2) 
        }) 
    return results, total_minutes, total_hours 
 
def read_existing_total(): 
    """Dosyadaki mevcut toplam süreyi dakika cinsinden döndürür, yoksa 0.""" 
    if not os.path.isfile(file_name): 
        return 0 
 
    with open(file_name, "r", encoding="utf-8") as f: 
        lines = f.readlines() 
 
    # Sadece en son 'Genel Toplam Süre' satırını bul 
    total_pattern = re.compile(r"Genel Toplam Süre:\s*(\d+)\s*dakika", 
re.IGNORECASE) 
    for line in reversed(lines): 
        match = total_pattern.search(line) 
        if match: 
            return int(match.group(1)) 
    return 0 
 
def remove_old_totals_and_trailing_separator(lines): 
    """Dosyadaki önceki toplam süre satırlarını ve eşit işaretli çizgiyi 
çıkarır.""" 
    new_lines = [] 
    skip_pattern = re.compile(r"^Toplam Süre:.*|^=+$") 
    for line in lines: 
        if skip_pattern.match(line.strip()): 
            continue 
        new_lines.append(line) 
    return new_lines 
 
def print_results_and_update_total(results, total_minutes_new, total_hours_new): 
    header = f"{'Başlangıç':<10} {'Bitiş':<10} {'Süre (dk)':<10} {'Süre (saat)':<12}" 
    separator = "-" * 45 
 
    # Mevcut dosya varsa oku 
    if os.path.isfile(file_name): 
        with open(file_name, "r", encoding="utf-8") as f: 
            existing_lines = f.readlines() 
        cleaned_lines = remove_old_totals_and_trailing_separator(existing_lines) 
    else: 
        cleaned_lines = [] 
 
    # Mevcut toplam dakika (önceden kaydedilmiş) 
    old_total_minutes = read_existing_total() 
 
    # Yeni girişe ait toplam 
    current_total_minutes = round(total_minutes_new) 
    current_total_hours = round(total_hours_new, 2) 
 
    # Güncellenmiş genel toplam 
    grand_total_minutes = old_total_minutes + current_total_minutes 
    grand_total_hours = round(grand_total_minutes / 60, 2) 
 
    # Dosyayı güncelle 
    with open(file_name, "w", encoding="utf-8") as f: 
        # Başlık 
        if not cleaned_lines: 
            f.write(header + "\n") 
            f.write(separator + "\n") 
        else: 
            for line in cleaned_lines: 
                f.write(line) 
 
        # Yeni girişleri ekle 
        for r in results: 
            f.write(f"{r['Başlangıç']:<10} {r['Bitiş']:<10} {r['Süre (dk)']:<10} {r['Süre (saat)']:<12}\n") 
 
        # Yeni girişin toplamı 
        f.write(f"\nToplam Süre (bu giriş): {current_total_minutes} dakika ({current_total_hours} saat)\n") 
        f.write("=" * 45 + "\n") 
 
        # Genel toplam süre (önceki + bu giriş) 
        f.write(f"\nGenel Toplam Süre: {grand_total_minutes} dakika ({grand_total_hours} saat)\n") 
 
    # Konsola yazdır 
    print("\n" + header) 
    print(separator) 
    for r in results: 
        print(f"{r['Başlangıç']:<10} {r['Bitiş']:<10} {r['Süre (dk)']:<10} {r['Süre (saat)']:<12}") 
    print(f"\nToplam Süre (bu giriş): {current_total_minutes} dakika ({current_total_hours} saat)") 
    print(f"Genel Toplam Süre (tüm kayıtlar): {grand_total_minutes} dakika ({grand_total_hours} saat)") 
def main(): 
    times = input_times() 
    results, total_minutes, total_hours = calculate_durations(times) 
    print_results_and_update_total(results, total_minutes, total_hours) 

if __name__ == "__main__": 
    main() 
