import requests
import time
from datetime import datetime

# ===== ISI DATA ANDA DI SINI =====
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
WEATHER_API_KEY = "YOUR_WEATHER_API_KEY"
KOTA = "Jakarta"
# =================================

def kirim_pesan(pesan):
    """Kirim pesan ke Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': pesan}
    try:
        requests.post(url, data=data)
        print(f"✓ Pesan terkirim")
    except:
        print("✗ Gagal kirim pesan")

def cek_cuaca():
    """Cek apakah sedang/akan hujan"""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': KOTA,
        'appid': WEATHER_API_KEY,
        'units': 'metric',
        'lang': 'id'
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Ambil informasi cuaca
        weather_id = data['weather'][0]['id']
        deskripsi = data['weather'][0]['description']
        suhu = data['main']['temp']
        
        # Cek apakah hujan (kode 2xx, 3xx, 5xx = hujan)
        if 200 <= weather_id < 600:
            pesan = f"🌧️ HUJAN DI {KOTA}!\n\n"
            pesan += f"Kondisi: {deskripsi}\n"
            pesan += f"Suhu: {suhu}°C\n"
            pesan += f"Waktu: {datetime.now().strftime('%H:%M')}"
            
            kirim_pesan(pesan)
            print(f"⚠️ Terdeteksi hujan!")
            return True
        else:
            print(f"✓ Tidak hujan ({deskripsi})")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

# Program utama
print("🤖 Bot Notifikasi Hujan")
print(f"Lokasi: {KOTA}")
print("Tekan Ctrl+C untuk berhenti\n")

# Kirim pesan bot aktif
kirim_pesan(f"✅ Bot aktif!\nMonitoring cuaca di {KOTA}")

# Loop utama - cek setiap 30 menit
while True:
    waktu = datetime.now().strftime('%H:%M:%S')
    print(f"[{waktu}] Mengecek cuaca...")
    
    cek_cuaca()
    
    # Tunggu 30 menit (1800 detik)
    print("Menunggu 30 menit...\n")
    time.sleep(1800)