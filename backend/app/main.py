from fastapi import FastAPI, WebSocket, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .models.campaign import Base, Campaign
from .services.payment_service import payment_service
from .services.xaman_service import xaman_service
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.engine import URL
from .config import settings

# Création de la base de données avec SQLite
engine = create_engine(
    "sqlite:///xrpl_music.db",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# Configuration CORS pour le développement
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency pour obtenir la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/auth/sign-request")
async def create_sign_request(user_token: str = None):
    """Crée une demande de signature pour la connexion via Xaman."""
    try:
        return await xaman_service.create_sign_request(user_token)
    except Exception as e:
        print(f"Error creating sign request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/auth/verify/{payload_uuid}")
async def verify_signature(payload_uuid: str):
    """Vérifie la signature d'une demande de connexion."""
    try:
        result = await xaman_service.verify_signature(payload_uuid)
        if result["success"]:
            return result
        raise HTTPException(status_code=401, detail="Signature non valide")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/campaigns/active")
async def get_active_campaigns(db: Session = Depends(get_db)):
    """Récupère toutes les campagnes actives"""
    campaigns = db.query(Campaign).filter(Campaign.status == "active").all()
    return campaigns

@app.post("/api/campaigns")
async def create_campaign(campaign_data: dict, db: Session = Depends(get_db)):
    """Crée une nouvelle campagne"""
    campaign = Campaign(
        artist_address=campaign_data["artistAddress"],
        song_title=campaign_data["songTitle"],
        song_url=campaign_data["songUrl"],
        total_amount=campaign_data["amount"],
        amount_per_second=settings.PAYMENT_PER_SECOND,
        remaining_amount=campaign_data["amount"],
        status="active"
    )
    db.add(campaign)
    db.commit()
    db.refresh(campaign)
    return campaign

@app.websocket("/ws/listen/{campaign_id}/{listener_address}")
async def websocket_endpoint(
    websocket: WebSocket,
    campaign_id: int,
    listener_address: str,
    db: Session = Depends(get_db)
):
    """Endpoint WebSocket pour le tracking d'écoute"""
    await websocket.accept()
    await payment_service.start_listening_session(
        websocket,
        campaign_id,
        listener_address,
        db
    ) 