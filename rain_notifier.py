import requests
import schedule
import time
from datetime import datetime

# ===== KONFIGURASI - ISI DATA ANDA DI SINI =====
# Segera ganti token ini di @BotFather karena yang lama sudah tidak aman
TELEGRAM_BOT_TOKEN = "8535850688:AAEqjNFbnPAZKb5Mp65o-b7EYDZxfeyQ2yk"
TELEGRAM_CHAT_ID = "1519188290"
OPENWEATHER_API_KEY = "d8b203c84ff7ce3821bd0ec5bf079255"

# Koordinat lokasi Anda (Jonggol/Cipeucang)
CITY_NAME = None 
LAT = -6.4537731
LON = 107.041207

# Interval pengecekan (dalam menit)
CHECK_INTERVAL = 5
# ===============================================

class RainNotifier:
    def __init__(self):
        self.last_rain_status = False
        self.base_weather_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    def get_weather_data(self):
        """Mengambil data cuaca terkini"""
        try:
            params = {
                'lat': LAT, 'lon': LON,
                'appid': OPENWEATHER_API_KEY,
                'units': 'metric', 'lang': 'id'
            } if not CITY_NAME else {
                'q': CITY_NAME, 'appid': OPENWEATHER_API_KEY,
                'units': 'metric', 'lang': 'id'
            }
            response = requests.get(self.base_weather_url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error cuaca: {e}")
            return None

    def get_forecast_data(self):
        """Mengambil data prediksi cuaca (forecast)"""
        try:
            params = {
                'lat': LAT, 'lon': LON,
                'appid': OPENWEATHER_API_KEY,
                'units': 'metric', 'lang': 'id', 'cnt': 5 # Cek beberapa baris ke depan
            }
            response = requests.get(self.forecast_url, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error forecast: {e}")
            return None

    def send_telegram_message(self, message):
        """Mengirim pesan ke Telegram dengan mode HTML"""
        try:
            data = {'chat_id': TELEGRAM_CHAT_ID, 'text': message, 'parse_mode': 'HTML', 'disable_web_page_preview': False}
            response = requests.post(self.telegram_url, data=data)
            return response.ok
        except Exception as e:
            print(f"Error Telegram: {e}")
            return False

    def is_raining(self, weather_data):
        """Cek ID cuaca untuk kategori hujan (200-599)"""
        if not weather_data or 'weather' not in weather_data:
            return False
        weather_id = weather_data['weather'][0]['id']
        return 200 <= weather_id < 600

    def get_rain_intensity(self, weather_data):
        """Mapping ID cuaca ke Emoji dan teks yang lebih informatif"""
        wid = weather_data['weather'][0]['id']
        if 200 <= wid < 300: return "⛈️ <b>Hujan Petir</b>"
        if 300 <= wid < 400: return "🌦️ <b>Gerimis</b>"
        if 500 <= wid <= 501: return "🌧️ <b>Hujan Ringan</b>"
        if 502 <= wid <= 503: return "🌧️ <b>Hujan Sedang</b>"
        if wid >= 504: return "🌧️ <b>Hujan Deras</b>"
        return "🌧️ <b>Hujan</b>"

    def check_weather(self):
        """Logika utama pengecekan cuaca"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Mengecek cuaca...")
        current = self.get_weather_data()
        if not current: return

        is_raining_now = self.is_raining(current)
        loc_name = current.get('name', 'Lokasi Tidak Diketahui')
        maps_url = f"https://www.google.com/maps?q={LAT},{LON}"

        # 1. Jika Baru Mulai Hujan
        if is_raining_now and not self.last_rain_status:
            intensity = self.get_rain_intensity(current)
            msg = (f"🌧️ <b>PERINGATAN HUJAN!</b>\n\n"
                   f"{intensity}\n"
                   f"📍 Wilayah: {loc_name}\n"
                   f"🌡️ Suhu: {current['main']['temp']}°C\n"
                   f"📝 Kondisi: {current['weather'][0]['description'].capitalize()}\n\n"
                   f"🌍 <a href='{maps_url}'>Lihat Peta Posisi</a>")
            self.send_telegram_message(msg)
            self.last_rain_status = True

        # 2. Jika Hujan Berhenti
        elif not is_raining_now and self.last_rain_status:
            msg = (f"☀️ <b>Hujan telah berhenti</b>\n"
                   f"📍 Wilayah: {loc_name}\n"
                   f"⏰ Waktu: {datetime.now().strftime('%H:%M')}")
            self.send_telegram_message(msg)
            self.last_rain_status = False

        # 3. Cek Prediksi (Jika sekarang belum hujan)
        elif not is_raining_now:
            forecast = self.get_forecast_data()
            if forecast and 'list' in forecast:
                for item in forecast['list'][:3]: # Cek 3-9 jam ke depan
                    if self.is_raining(item):
                        f_time = datetime.fromtimestamp(item['dt'])
                        intensity = self.get_rain_intensity(item)
                        msg = (f"⚠️ <b>PREDIKSI HUJAN</b>\n\n"
                               f"{intensity}\n"
                               f"📍 Wilayah: {loc_name}\n"
                               f"🕐 Estimasi: {f_time.strftime('%H:%M')} WIB\n\n"
                               f"Siapkan payung atau jemuran! ☂️")
                        self.send_telegram_message(msg)
                        break 
        
        print(f"Status: {'Hujan' if is_raining_now else 'Cerah/Berawan'}")

def main():
    print("=" * 50)
    print("🤖 BOT NOTIFIKASI HUJAN AKTIF")
    print("=" * 50)
    
    notifier = RainNotifier()
    
    # Pesan pembuka saat bot dijalankan
    start_msg = (f"✅ <b>Bot Notifikasi Hujan Berhasil Dijalankan</b>\n\n"
                 f"📍 Koordinat: {LAT}, {LON}\n"
                 f"🔄 Interval: {CHECK_INTERVAL} menit\n"
                 f"🚀 Status: Monitoring aktif...")
    notifier.send_telegram_message(start_msg)

    # Jalankan sekali saat startup
    notifier.check_weather()

    # Penjadwalan
    schedule.every(CHECK_INTERVAL).minutes.do(notifier.check_weather)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Bot dimatikan.")

if __name__ == "__main__":
    main()