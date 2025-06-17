import os
from flask import Flask
import requests
import random
from datetime import datetime
import time
from threading import Thread

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# 🔍 Real Data Fetching Function (Simulated for now)
def fetch_real_data():
    return [random.randint(0, 9) for _ in range(100)]  # Future: replace with live scraper

# 🤖 Prediction Logic (Simple for now)
def train_and_predict(data):
    return max(set(data), key=data.count)

# ✅ Send Result to Telegram
def send_to_telegram(prediction):
    color = "Green" if prediction % 2 == 0 else "Red"
    size = "Big" if prediction >= 5 else "Small"
    message = (
        f"📢 Wingo Prediction\n"
        f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"🎯 Result: {prediction} ({size}, {color})"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    response = requests.post(url, data={"chat_id": CHAT_ID, "text": message})
    print("Telegram sent:", response.status_code)

# 🌐 Home Page Route
@app.route('/')
def home():
    return "✅ Wingo Predictor Bot Is Running!"

# 🧪 Manual Prediction Trigger
@app.route('/predict')
def predict_route():
    data = fetch_real_data()
    pred = train_and_predict(data)
    send_to_telegram(pred)
    return f"✅ Prediction sent: {pred}"

# 🔁 Background Scheduler for Auto Prediction
def prediction_scheduler():
    while True:
        try:
            data = fetch_real_data()
            pred = train_and_predict(data)
            send_to_telegram(pred)
            time.sleep(60)  # প্রতি ১ মিনিটে
        except Exception as e:
            print("Scheduler Error:", e)
            time.sleep(10)

# 🚀 Start Flask + Background Scheduler
if __name__ == "__main__":
    Thread(target=prediction_scheduler).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
