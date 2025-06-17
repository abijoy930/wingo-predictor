import os
from flask import Flask
import requests
import random
from datetime import datetime
import time
from threading import Thread

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

def fetch_real_data():
    return [random.randint(0, 9) for _ in range(100)]

def train_and_predict(data):
    return max(set(data), key=data.count)

def send_to_telegram(prediction):
    color = "Green" if prediction % 2 == 0 else "Red"
    big_small = "Big" if prediction >= 5 else "Small"
    msg = f"📊 Prediction at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nResult: {prediction} ({big_small}, {color})"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

@app.route('/')
def home():
    return "✅ Wingo Predictor Bot Is Running!"

@app.route('/predict')
def predict_route():
    data = fetch_real_data()
    pred = train_and_predict(data)
    send_to_telegram(pred)
    return f"✅ Prediction sent: {pred}"

def prediction_scheduler():
    while True:
        try:
            data = fetch_real_data()
            pred = train_and_predict(data)
            send_to_telegram(pred)
            time.sleep(60)  # প্রতি ১ মিনিট পর পর
        except Exception as e:
            print(f"Error in scheduler: {e}")
            time.sleep(10)

if __name__ == "__main__":
    Thread(target=prediction_scheduler).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
