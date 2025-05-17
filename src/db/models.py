from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class OrderStatus(enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

class OrderType(enum.Enum):
    BID = "bid"
    ASK = "ask"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    bids = relationship("Order", back_populates="bidder", foreign_keys="Order.bidder_id")
    asks = relationship("Order", back_populates="seller", foreign_keys="Order.seller_id")
    auctions = relationship("Auction", back_populates="creator")

class Auction(Base):
    __tablename__ = "auctions"

    id = Column(Integer, primary_key=True, index=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    nft_token_id = Column(String, index=True)
    title = Column(String)
    description = Column(String)
    starting_price = Column(Float)
    min_bid_increment = Column(Float)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(Enum(OrderStatus))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relations
    creator = relationship("User", back_populates="auctions")
    orders = relationship("Order", back_populates="auction")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    auction_id = Column(Integer, ForeignKey("auctions.id"))
    bidder_id = Column(Integer, ForeignKey("users.id"))
    seller_id = Column(Integer, ForeignKey("users.id"))
    order_type = Column(Enum(OrderType))
    price = Column(Float)
    status = Column(Enum(OrderStatus))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    auction = relationship("Auction", back_populates="orders")
    bidder = relationship("User", back_populates="bids", foreign_keys=[bidder_id])
    seller = relationship("User", back_populates="asks", foreign_keys=[seller_id]) 