import requests
import os

# Mengambil 'Kunci' dari brankas GitHub Secrets
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_KEY")

LAT = -6.4537731
LON = 107.041207

def check_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={OPENWEATHER_API_KEY}&units=metric&lang=id"
    response = requests.get(url).json()
    
    # Ambil info cuaca
    weather_desc = response['weather'][0]['description']
    temp = response['main']['temp']
    
    # PESAN TES: Supaya kamu tahu bot ini kerja
    msg = f"🤖 <b>LAPORAN BOT JONGGOL</b>\n\nKondisi: {weather_desc}\nSuhu: {temp}°C\nStatus: Koneksi Berhasil!"

    # Kirim ke Telegram
    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    requests.post(api_url, data={'chat_id': TELEGRAM_CHAT_ID, 'text': msg, 'parse_mode': 'HTML'})
    print(f"Berhasil! Cuaca saat ini: {weather_desc}")

if __name__ == "__main__":
    check_weather()