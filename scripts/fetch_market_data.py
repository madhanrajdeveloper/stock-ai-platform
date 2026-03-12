import os
import sys
import django
import yfinance as yf

# Setup Django
sys.path.append("../backend")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from stocks.models import Stock, MarketData


def fetch_stock_data(symbol):

    data = yf.download(symbol, period="3mo", interval="1d")

    # flatten columns if multi-index
    if hasattr(data.columns, "levels"):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()

    return data


def save_market_data(stock, data):

    for _, row in data.iterrows():

        try:

            open_price = float(row.Open)
            high_price = float(row.High)
            low_price = float(row.Low)
            close_price = float(row.Close)
            volume = int(row.Volume)

            MarketData.objects.update_or_create(
                stock=stock,
                date=row.Date.date(),
                defaults={
                    "open_price": open_price,
                    "high_price": high_price,
                    "low_price": low_price,
                    "close_price": close_price,
                    "volume": volume,
                },
            )

        except Exception as e:

            print("Row skipped:", e)


def run():

    stocks = Stock.objects.all()

    for stock in stocks:

        print("Fetching:", stock.symbol)

        try:

            data = fetch_stock_data(stock.symbol)

            if not data.empty:

                save_market_data(stock, data)

                print("Saved data for:", stock.symbol)

        except Exception as e:

            print("Error:", e)


if __name__ == "__main__":
    run()