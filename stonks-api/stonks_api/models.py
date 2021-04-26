from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import ARRAY

Base = declarative_base()


class Fee(Base):
    __tablename__ = "fee"

    id = Column(Integer, primary_key=True, autoincrement=True)

    stonks_id = Column(Integer, ForeignKey("stonks.id", ondelete="CASCADE"), nullable=False)
    stonks = relationship("Stonks", back_populates="fees")

    title = Column(String, nullable=False)
    amount = Column(Numeric(15, 4), nullable=False)
    currency = Column(String(3), nullable=False)


class Delivery(Base):
    __tablename__ = "delivery"

    id = Column(Integer, primary_key=True, autoincrement=True)

    offer_id = Column(String, ForeignKey("offer.id", ondelete="CASCADE"), nullable=False)
    offer = relationship("Offer", back_populates="deliveries")

    title = Column(String, nullable=True)
    price = Column(Numeric(15, 4), nullable=False)
    currency = Column(String(3), nullable=False)


class Offer(Base):
    __tablename__ = "offer"

    id = Column(String, primary_key=True, nullable=False)

    url = Column(String)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String(32), nullable=False)

    price = Column(Numeric(15, 4), nullable=False)
    currency = Column(String(3), nullable=False)

    deliveries = relationship("Delivery", back_populates="offer")

    photos = Column(ARRAY(String))
    is_active = Column(Boolean, nullable=False)

    last_refresh_time = Column(DateTime)
    last_scraped_time = Column(DateTime, nullable=False)


class Stonks(Base):
    __tablename__ = "stonks"

    id = Column(Integer, primary_key=True, autoincrement=True)

    offer_id = Column(String, ForeignKey("offer.id", ondelete="CASCADE"), nullable=False)
    offer = relationship("Offer", uselist=False)

    fees = relationship("Fee", back_populates="stonks")

    low_price = Column(Numeric(15, 4), nullable=False)
    high_price = Column(Numeric(15, 4), nullable=False)
    average_price = Column(Numeric(15, 4), nullable=False)
    median_price = Column(Numeric(15, 4), nullable=False)
    harmonic_price = Column(Numeric(15, 4), nullable=False)
