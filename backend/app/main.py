from fastapi import FastAPI
from app.services.coingecko_service import fetch_market_data
from app.database.database import engine
from app.models.market import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Crypto Analytics API Running"}


@app.get("/markets")
async def get_markets():
    return fetch_market_data()