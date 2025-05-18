from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.campaign import Campaign
from app.models.listening import ListeningSession
from app.config import settings

router = APIRouter()

@router.delete("/campaigns/{campaign_id}")
def delete_campaign(
    campaign_id: int,
    artist_address: str,
    db: Session = Depends(get_db)
):
    """Supprime une campagne"""
    campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
    
    if not campaign:
        raise HTTPException(status_code=404, detail="Campagne non trouvée")
        
    if campaign.artist_address != artist_address:
        raise HTTPException(
            status_code=403,
            detail="Vous n'êtes pas autorisé à supprimer cette campagne"
        )
    
    # Vérifier s'il y a des sessions d'écoute actives
    active_sessions = db.query(ListeningSession).filter(
        ListeningSession.campaign_id == campaign_id,
        ListeningSession.end_time.is_(None)
    ).all()
    
    if active_sessions:
        raise HTTPException(
            status_code=400,
            detail="Impossible de supprimer la campagne car il y a des sessions d'écoute en cours"
        )
    
    # Supprimer d'abord toutes les sessions d'écoute terminées
    db.query(ListeningSession).filter(
        ListeningSession.campaign_id == campaign_id,
        ListeningSession.end_time.isnot(None)
    ).delete(synchronize_session=False)
    
    # Puis supprimer la campagne
    db.delete(campaign)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la suppression de la campagne: {str(e)}"
        )
    
    return {"message": "Campagne supprimée avec succès"}

@router.get("/campaigns/active", response_model=List[dict])
def get_active_campaigns(db: Session = Depends(get_db)):
    """Récupère toutes les campagnes actives"""
    campaigns = db.query(Campaign).filter(Campaign.status == "active").all()
    return [campaign.to_dict() for campaign in campaigns]

@router.post("/campaigns", response_model=dict)
def create_campaign(campaign_data: dict, db: Session = Depends(get_db)):
    """Crée une nouvelle campagne"""
    try:
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
        return campaign.to_dict()
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Données manquantes: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la création de la campagne: {str(e)}"
        ) 