import os
from flask import Flask
import requests
import random
from datetime import datetime

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
    msg = f"🎯 Prediction at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nResult: {prediction} ({big_small}, {color})"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

@app.route('/')
def home():
    return "✅ Wingo Predictor Bot is Running!"

@app.route('/predict')
def predict_route():
    data = fetch_real_data()
    pred = train_and_predict(data)
    send_to_telegram(pred)
    return f"✅ Prediction sent: {pred}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
