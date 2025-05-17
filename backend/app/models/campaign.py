from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True, index=True)
    artist_address = Column(String, index=True)
    song_title = Column(String)
    song_url = Column(String)
    total_amount = Column(Float)  # Montant total en XRP
    amount_per_second = Column(Float)  # Montant par seconde d'écoute
    remaining_amount = Column(Float)  # Montant restant à distribuer
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String)  # active, completed, cancelled

    # Relations
    listeners = relationship("CampaignListener", back_populates="campaign")

class CampaignListener(Base):
    __tablename__ = "campaign_listeners"

    id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey("campaigns.id"))
    listener_address = Column(String, index=True)
    seconds_listened = Column(Integer, default=0)
    amount_earned = Column(Float, default=0.0)
    last_payment_time = Column(DateTime)
    status = Column(String)  # active, completed

    # Relations
    campaign = relationship("Campaign", back_populates="listeners") 