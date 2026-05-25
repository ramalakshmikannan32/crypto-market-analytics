from sqlalchemy.orm import Session
from app.models.market import Market


def calculate_analytics(db: Session):
    symbols = db.query(Market.symbol).distinct().all()

    results = []

    for symbol_tuple in symbols:
        symbol = symbol_tuple[0]

        records = (
            db.query(Market)
            .filter(Market.symbol == symbol)
            .order_by(Market.timestamp.desc())
            .limit(2)
            .all()
        )

        if len(records) < 2:
            continue

        latest = records[0]
        previous = records[1]

        price_change = (
            ((latest.price - previous.price) / previous.price) * 100
        )

        volume_change = (
            ((latest.volume - previous.volume) / previous.volume) * 100
        )

        results.append({
            "symbol": symbol,
            "latest_price": latest.price,
            "previous_price": previous.price,
            "price_change_percent": round(price_change, 2),
            "volume_change_percent": round(volume_change, 2)
        })

    return results