import requests
import time
from telegram import Bot
from datetime import datetime
import os

# Lấy token và chat_id từ biến môi trường (Render sẽ cung cấp)
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = Bot(token=BOT_TOKEN)

def get_price_xau():
    try:
        response = requests.get('https://api.metals.live/v1/spot')
        data = response.json()
        for item in data:
            if 'gold' in item:
                return float(item['gold'])
    except:
        return None

def get_price_btc():
    try:
        response = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT')
        return float(response.json()['price'])
    except:
        return None

def send_price():
    xau = get_price_xau()
    btc = get_price_btc()
    now = datetime.now().strftime("%H:%M %d/%m/%Y")

    message = f"🕒 {now}\n\n"
    message += f"Giá XAUUSD: {'${:,.2f}'.format(xau) if xau else 'Không lấy được'}\n"
    message += f"Giá BTC: {'${:,.2f}'.format(btc) if btc else 'Không lấy được'}"

    bot.send_message(chat_id=CHAT_ID, text=message)

# Bot chỉ hoạt động từ 07:00 Thứ 2 đến 23:00 Thứ 6
while True:
    now = datetime.now()
    weekday = now.weekday()  # 0 = Monday, 6 = Sunday

    if 0 <= weekday <= 4 and 7 <= now.hour < 23:
        send_price()
    else:
        print(f"[{now.strftime('%a %H:%M')}] Ngoài giờ hoạt động, bot đang nghỉ...")

    time.sleep(3600)
