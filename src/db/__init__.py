from .models import Base, User, Auction, Order, OrderStatus, OrderType
from .database import engine, SessionLocal, get_db
from .crud import DatabaseManager

# Créer les tables au démarrage
Base.metadata.create_all(bind=engine)
