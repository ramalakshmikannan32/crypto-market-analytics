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

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Crypto Analytics API Running"}


@app.get("/markets")
async def get_markets():
    return fetch_market_data()


@app.post("/markets/save")
async def save_markets(db: Session = Depends(get_db)):
    return save_market_data(db)

@app.get("/history")
async def market_history(
    symbol: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return get_market_history(db, symbol, limit)

@app.get("/analytics")
async def analytics(db: Session = Depends(get_db)):
    return calculate_analytics(db)

@app.post("/strategy/run")
async def execute_strategy(db: Session = Depends(get_db)):
    return run_strategy(db)


@app.get("/strategy/results")
async def strategy_results():
    return get_strategy_results()