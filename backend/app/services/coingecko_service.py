import requests
from sqlalchemy.orm import Session

from app.models.market import Market

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT"]


def fetch_market_data():
    results = []

    for symbol in SYMBOLS:
        response = requests.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}")
        data = response.json()

        results.append({
            "symbol": symbol.replace("USDT", "").lower(),
            "name": symbol.replace("USDT", ""),
            "price": float(data["lastPrice"]),
            "volume": float(data["volume"]),
        })

    return results


def save_market_data(db: Session):
    data = fetch_market_data()

    for coin in data:
        market = Market(
            symbol=coin["symbol"],
            name=coin["name"],
            price=coin["price"],
            volume=coin["volume"]
        )

        db.add(market)

    db.commit()

    return {"message": "Market data saved successfully"}


def get_market_history(db: Session, symbol: str, limit: int):
    history = (
        db.query(Market)
        .filter(Market.symbol == symbol.lower())
        .order_by(Market.timestamp.desc())
        .limit(limit)
        .all()
    )

    return history