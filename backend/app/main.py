from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.database.database import engine
from fastapi.middleware.cors import CORSMiddleware
from app.database.session import get_db
from app.analytics.market_analytics import calculate_analytics
from app.strategy.market_strategy import (
    run_strategy,
    get_strategy_results
)
from app.models.market import Base
from app.services.coingecko_service import (
    fetch_market_data,
    save_market_data,
    get_market_history
)

Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.database.session import SessionLocal
    db = SessionLocal()
    try:
        save_market_data(db)
    except Exception:
        pass
    finally:
        db.close()
    yield


app = FastAPI(
    title="Crypto Market Analytics API",
    description="Real-time cryptocurrency analytics platform with market history, analytics engine, and trading strategy signals.",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["System"])
async def root():
    return {"message": "Crypto Analytics API Running"}


@app.get("/markets", tags=["Markets"])
async def get_markets():
    return fetch_market_data()


@app.post("/markets/save", tags=["Markets"])
async def save_markets(db: Session = Depends(get_db)):
    return save_market_data(db)

@app.get("/markets/stored", tags=["Markets"])
async def get_stored_markets(db: Session = Depends(get_db)):
    from app.models.market import Market
    return db.query(Market).order_by(Market.timestamp.desc()).all()


@app.get("/history", tags=["History"])
async def market_history(
    symbol: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_market_history(db, symbol, limit)

@app.get("/analytics", tags=["Analytics"])
async def analytics(db: Session = Depends(get_db)):
    return calculate_analytics(db)

@app.post("/strategy/run", tags=["Strategy"])
async def execute_strategy(db: Session = Depends(get_db)):
    return run_strategy(db)


@app.get("/strategy/results", tags=["Strategy"])
async def strategy_results():
    return get_strategy_results()