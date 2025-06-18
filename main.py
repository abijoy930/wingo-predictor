import telegram
from flask import Flask

# ✅ Replace these with your real bot token and chat ID
TELEGRAM_BOT_TOKEN = "7751314755:AAFXmYJ2lW7xZhU7Txl1JuqCxG8LfbKmNZM"
CHAT_ID = "6848807471"

bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def send_telegram_message(text):
    try:
        bot.send_message(chat_id=CHAT_ID, text=text)
        print("✅ Telegram message sent!")
    except Exception as e:
        print("❌ Telegram error:", e)

# ✅ Send a message when service starts
send_telegram_message("✅ Wingo Prediction Bot is now LIVE on Render!")

# 🛰️ Basic Flask setup (so Render can keep it live)
app = Flask(__name__)

@app.route('/')
def home():
    return 'Wingo Predictor is live!'

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)
