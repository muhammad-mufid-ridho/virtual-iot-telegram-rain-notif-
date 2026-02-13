import requests
from datetime import datetime

# KONFIGURASI (Ganti dengan Token/ID Anda)
TELEGRAM_BOT_TOKEN = "8535850688:AAEqjNFbnPAZKb5Mp65o-b7EYDZxfeyQ2yk"
TELEGRAM_CHAT_ID = "1519188290"
OPENWEATHER_API_KEY = "d8b203c84ff7ce3821bd0ec5bf079255"
LAT = -6.4537731
LON = 107.041207

def check_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={OPENWEATHER_API_KEY}&units=metric&lang=id"
    response = requests.get(url).json()
    
    weather_id = response['weather'][0]['id']
    is_raining = 200 <= weather_id < 600
    
    if is_raining:
        msg = f"🌧️ <b>PERINGATAN HUJAN!</b>\n\nKondisi: {response['weather'][0]['description']}\nLokasi: {response['name']}"
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", 
                      data={'chat_id': TELEGRAM_CHAT_ID, 'text': msg, 'parse_mode': 'HTML'})
        print("Notifikasi hujan dikirim.")
    else:
        print("Cuaca cerah, tidak ada pesan dikirim.")

if __name__ == "__main__":
    check_weather()