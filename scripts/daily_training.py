import os
import sys
import django
import pandas as pd
import joblib

from sklearn.linear_model import LinearRegression

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR + "/backend")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django.setup()

from stocks.models import Stock, MarketData

import ta


MODEL_DIR = os.path.join(BASE_DIR, "models")

os.makedirs(MODEL_DIR, exist_ok=True)


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

    features = [
        "open_price",
        "high_price",
        "low_price",
        "volume",
        "rsi",
        "ma20",
        "ma50",
        "macd",
        "bb_high",
        "bb_low",
    ]

    X = df[features]

    y = df["close_price"]

    model = LinearRegression()

    model.fit(X, y)

    model_path = os.path.join(MODEL_DIR, f"{stock.symbol}.pkl")

    joblib.dump(model, model_path)

    print("Model trained:", stock.symbol)