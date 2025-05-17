from xumm import XummSdk
from ..config import settings

class XamanService:
    def __init__(self):
        self.sdk = XummSdk(
            settings.XAMAN_API_KEY,
            settings.XAMAN_API_SECRET
        )

    async def create_sign_request(self, user_token: str = None) -> dict:
        """Crée une demande de signature pour la connexion."""
        payload = {
            "txjson": {
                "TransactionType": "SignIn"
            }
        }
        
        if user_token:
            payload["user_token"] = user_token
            
        response = self.sdk.payload.create(payload)
        return {
            "qr_url": response.refs.qr_png,
            "websocket_url": response.refs.websocket_status,
            "payload_uuid": response.uuid
        }

    async def verify_signature(self, payload_uuid: str) -> dict:
        """Vérifie la signature d'une demande de connexion."""
        try:
            response = self.sdk.payload.get(payload_uuid)
        
            if response.meta.signed:
                return {
                "success": True,
                    "account": response.response.account,
                    "user_token": response.application.issued_user_token
                }
        except Exception as e:
            print(f"Error verifying signature: {e}")
        return {"success": False}

xaman_service = XamanService() 