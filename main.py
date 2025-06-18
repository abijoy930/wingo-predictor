import os
import requests
import time
from datetime import datetime
from threading import Thread
from flask import Flask
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense

app = Flask(__name__)

# Telegram Bot Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# Dummy data fetcher - replace with real scraper if needed
def fetch_data():
    return np.random.randint(0, 10, size=100).tolist()

# Prepare data for LSTM
def prepare_data(data, n_steps=10):
    X, y = [], []
    for i in range(len(data) - n_steps):
        seq_x = data[i:i+n_steps]
        seq_y = data[i+n_steps]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)

# Build LSTM model
def build_model():
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(10, 1)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

# Send message to Telegram
def send_to_telegram(pred, confidence):
    color = "Green" if pred % 2 == 0 else "Red"
    size = "Big" if pred >= 5 else "Small"
    alert = "🔔 High Confidence!" if confidence >= 90 else ""
    msg = f"📊 Prediction: {datetime.now().strftime('%H:%M:%S')}\nResult: {pred} ({size}, {color})\nConfidence: {confidence:.2f}%\n{alert}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# Main prediction loop
def predictor_loop():
    while True:
        try:
            data = fetch_data()
            X, y = prepare_data(data)
            X = X.reshape((X.shape[0], X.shape[1], 1))
            model = build_model()
            model.fit(X, y, epochs=10, verbose=0)
            x_input = np.array(data[-10:]).reshape((1, 10, 1))
            yhat = model.predict(x_input, verbose=0)
            pred = int(round(yhat[0][0]))
            pred = max(0, min(9, pred))  # Clamp between 0 and 9
            confidence = 100 - abs(pred - np.mean(y)) * 10  # crude confidence
            send_to_telegram(pred, confidence)
            time.sleep(60)
        except Exception as e:
            print("Error in prediction:", e)
            time.sleep(10)

# Flask route
@app.route('/')
def home():
    return "✅ Wingo Predictor Bot is running!"

if __name__ == "__main__":
    Thread(target=predictor_loop).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
