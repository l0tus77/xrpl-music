from datetime import datetime
from fastapi import WebSocket
import asyncio
from .xrpl_service import xrpl_service
from ..models.campaign import Campaign, CampaignListener
from sqlalchemy.orm import Session

class PaymentService:
    def __init__(self):
        self.active_listeners = {}  # {websocket_id: {campaign_id, listener_address, last_payment}}

    async def start_listening_session(self, websocket: WebSocket, campaign_id: int, 
                                    listener_address: str, db: Session):
        """Démarre une session d'écoute pour un utilisateur."""
        session_id = id(websocket)
        campaign = db.query(Campaign).filter(Campaign.id == campaign_id).first()
        
        if not campaign or campaign.status != "active":
            await websocket.close()
            return

        self.active_listeners[session_id] = {
            "campaign_id": campaign_id,
            "listener_address": listener_address,
            "last_payment": datetime.utcnow(),
            "websocket": websocket
        }

        try:
            while True:
                # Attendre le message de heartbeat du client
                data = await websocket.receive_text()
                if data == "playing":
                    await self._process_payment(session_id, db)
                await asyncio.sleep(1)  # Attendre 1 seconde
        except Exception as e:
            print(f"Error in listening session: {e}")
        finally:
            if session_id in self.active_listeners:
                del self.active_listeners[session_id]

    async def _process_payment(self, session_id: str, db: Session):
        """Traite le paiement pour une seconde d'écoute."""
        listener_data = self.active_listeners[session_id]
        campaign = db.query(Campaign).filter(
            Campaign.id == listener_data["campaign_id"]
        ).first()

        if not campaign or campaign.remaining_amount <= 0:
            await listener_data["websocket"].close()
            return

        # Calculer le montant à payer
        amount_to_pay = min(campaign.amount_per_second, campaign.remaining_amount)
        
        # Effectuer le paiement
        payment_result = await xrpl_service.send_payment(
            listener_data["listener_address"], 
            amount_to_pay
        )

        if payment_result["status"] == "success":
            # Mettre à jour la campagne et l'auditeur
            campaign.remaining_amount -= amount_to_pay
            
            listener = db.query(CampaignListener).filter(
                CampaignListener.campaign_id == campaign.id,
                CampaignListener.listener_address == listener_data["listener_address"]
            ).first()
            
            if listener:
                listener.seconds_listened += 1
                listener.amount_earned += amount_to_pay
                listener.last_payment_time = datetime.utcnow()
            
            db.commit()

payment_service = PaymentService() 