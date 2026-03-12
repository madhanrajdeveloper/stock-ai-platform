import os
import sys
import django
import pandas as pd
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR + "/backend")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django.setup()

from stocks.models import Stock, MarketData
from predictions.models import Prediction

import ta


MODEL_DIR = os.path.join(BASE_DIR, "models")

stocks = Stock.objects.all()

for stock in stocks:

    data = MarketData.objects.filter(stock=stock).order_by("date")

    df = pd.DataFrame(list(data.values()))

    if len(df) < 50:
        continue

    df["rsi"] = ta.momentum.RSIIndicator(df["close_price"]).rsi()

    df["ma20"] = df["close_price"].rolling(window=20).mean()

    df["ma50"] = df["close_price"].rolling(window=50).mean()

    macd = ta.trend.MACD(df["close_price"])

    df["macd"] = macd.macd()

    bb = ta.volatility.BollingerBands(df["close_price"])

    df["bb_high"] = bb.bollinger_hband()

    df["bb_low"] = bb.bollinger_lband()

    df = df.dropna()

    latest = df.iloc[-1]

    features = pd.DataFrame([{
        "open_price": latest.open_price,
        "high_price": latest.high_price,
        "low_price": latest.low_price,
        "volume": latest.volume,
        "rsi": latest.rsi,
        "ma20": latest.ma20,
        "ma50": latest.ma50,
        "macd": latest.macd,
        "bb_high": latest.bb_high,
        "bb_low": latest.bb_low,
    }])

    model_path = os.path.join(MODEL_DIR, f"{stock.symbol}.pkl")

    if not os.path.exists(model_path):
        continue

    model = joblib.load(model_path)

    prediction = model.predict(features)[0]

    Prediction.objects.create(
        stock=stock,
        predicted_close=prediction,
        prediction_type="daily",
        confidence=0.75,
    )

    print("Prediction saved:", stock.symbol)