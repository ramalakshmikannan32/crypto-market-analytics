# Crypto Analytics Dashboard

A full-stack cryptocurrency analytics platform built using FastAPI, Next.js, SQLite, and Binance API.

The platform provides real-time cryptocurrency market tracking, historical analytics, trading strategy signals, and interactive dashboard visualizations.

---

## Features

- Live cryptocurrency market data
- Historical market data storage
- Analytics engine for price and volume changes
- Moving average trading strategy signals
- Interactive charts and dashboard
- Search and filter functionality
- Auto-refreshing live data
- Responsive modern UI

---

## Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- Binance API

### Frontend
- Next.js
- React
- Tailwind CSS
- Recharts

---

## Architecture

Binance API → FastAPI Backend → SQLite Database → Analytics & Strategy Engine → Next.js Frontend Dashboard

---

## Backend APIs

### Market APIs
- GET /markets
- POST /markets/save
- GET /markets/stored

### Historical APIs
- GET /history

### Analytics APIs
- GET /analytics

### Strategy APIs
- POST /strategy/run
- GET /strategy/results

---

## Strategy Logic

The project uses a Moving Average crossover strategy.

- Short Moving Average > Long Moving Average → BUY
- Short Moving Average < Long Moving Average → SELL
- Equal → HOLD

---

## Installation

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload