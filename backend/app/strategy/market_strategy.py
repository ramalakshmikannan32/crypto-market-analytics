from sqlalchemy.orm import Session
from app.models.market import Market

strategy_results = []


def run_strategy(db: Session):
    global strategy_results

    strategy_results = []

    symbols = db.query(Market.symbol).distinct().all()

    for symbol_tuple in symbols:
        symbol = symbol_tuple[0]

        records = (
            db.query(Market)
            .filter(Market.symbol == symbol)
            .order_by(Market.timestamp.desc())
            .limit(5)
            .all()
        )

        if len(records) < 5:
            continue

        prices = [record.price for record in records]

        short_ma = sum(prices[:2]) / 2
        long_ma = sum(prices) / 5

        signal = "HOLD"

        if short_ma > long_ma:
            signal = "BUY"
        elif short_ma < long_ma:
            signal = "SELL"

        strategy_results.append({
            "symbol": symbol,
            "short_ma": round(short_ma, 2),
            "long_ma": round(long_ma, 2),
            "signal": signal
        })

    return strategy_results


def get_strategy_results():
    return strategy_results