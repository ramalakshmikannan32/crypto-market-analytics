from sqlalchemy import Column, Integer, String, Float
from app.database.database import Base


class Market(Base):
    __tablename__ = "markets"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    name = Column(String)
    price = Column(Float)
    volume = Column(Float)