from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./xrpl_music.db")
    XRPL_NODE_URL: str = os.getenv("XRPL_NODE_URL", "wss://s.altnet.rippletest.net:51233")
    XRPL_COLD_WALLET: str = ""  # Wallet principal pour les paiements
    XRPL_HOT_WALLET_SEED: str = os.getenv("XRPL_HOT_WALLET_SEED", "")
    PAYMENT_PER_SECOND: float = float(os.getenv("PAYMENT_PER_SECOND", "0.001"))
    MIN_CAMPAIGN_AMOUNT: float = float(os.getenv("MIN_CAMPAIGN_AMOUNT", "20.0"))
    
    # Configuration Xaman (XUMM)
    XAMAN_API_KEY: str = os.getenv("XAMAN_API_KEY", "")
    XAMAN_API_SECRET: str = os.getenv("XAMAN_API_SECRET", "")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings() 