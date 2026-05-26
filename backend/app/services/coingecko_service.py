import requests
from sqlalchemy.orm import Session

from app.models.market import Market

COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"


def fetch_market_data():
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1
    }

    response = requests.get(COINGECKO_URL, params=params)
    data = response.json()

    if not isinstance(data, list):
        print("CoinGecko API Error:", data)
        return []

    return data


def save_market_data(db: Session):
    data = fetch_market_data()

    for coin in data:
        market = Market(
            symbol=coin["symbol"],
            name=coin["name"],
            price=coin["current_price"],
            volume=coin["total_volume"]
        )
        db.add(market)

    db.commit()
    return {"message": "Market data saved successfully"}


def get_market_history(db: Session, symbol: str, limit: int):
    return (
        db.query(Market)
        .filter(Market.symbol == symbol.lower())
        .order_by(Market.timestamp.desc())
        .limit(limit)
        .all()
    )
