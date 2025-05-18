from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models import Tx
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops, drops_to_xrp
from xrpl.transaction import submit_and_wait
from ..config import settings
import asyncio

class XRPLService:
    def __init__(self):
        print("Initialisation du service XRPL...")
        print("URL du nœud XRPL:", settings.XRPL_NODE_URL)
        try:
            self.client = JsonRpcClient(settings.XRPL_NODE_URL)
            print("Client XRPL initialisé avec succès")
        except Exception as e:
            print(f"Erreur lors de l'initialisation du client XRPL: {type(e).__name__} - {str(e)}")
            raise
        
        try:
            self.hot_wallet = Wallet.from_seed(settings.XRPL_HOT_WALLET_SEED)
            print("Hot wallet initialisé avec succès")
        except Exception as e:
            print(f"Erreur lors de l'initialisation du hot wallet: {type(e).__name__} - {str(e)}")
            raise

    async def send_payment(self, destination: str, amount: float) -> dict:
        """Envoie un paiement en XRP à un destinataire."""
        payment = Payment(
            account=self.hot_wallet.classic_address,
            destination=destination,
            amount=xrp_to_drops(amount)
        )
        
        try:
            response = await asyncio.to_thread(submit_and_wait, payment, self.client, self.hot_wallet)
            return {
                "status": "success",
                "transaction_hash": response.result["hash"],
                "amount": amount
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    async def verify_transaction(self, transaction_hash: str, max_attempts: int = 5) -> dict:
        """Vérifie une transaction sur le XRPL avec plusieurs tentatives."""
        try:
            print(f"Début de la vérification XRPL pour hash: {transaction_hash}")
            
            for attempt in range(max_attempts):
                print(f"Tentative {attempt + 1}/{max_attempts}")
                
                response = await asyncio.to_thread(self.client.request, Tx(transaction=transaction_hash))
                print(f"Réponse XRPL brute: {response}")

                if hasattr(response, 'result'):
                    # Vérifier si la transaction est validée
                    if response.result.get('validated', False):
                        tx_json = response.result.get('tx_json', {})
                        meta = response.result.get('meta', {})
                        
                        if tx_json.get("TransactionType") == "Payment":
                            # Récupérer le montant depuis meta.delivered_amount si disponible
                            amount = meta.get('delivered_amount', tx_json.get('DeliverMax'))
                            if amount:
                                # Si le montant est une chaîne, c'est des drops
                                if isinstance(amount, str):
                                    amount = drops_to_xrp(amount)
                                return {
                                    "status": "success",
                                    "amount": float(amount),
                                    "sender": tx_json.get("Account"),
                                    "destination": tx_json.get("Destination")
                                }
            
                # Si on arrive ici et qu'il reste des tentatives, attendre avant de réessayer
                if attempt < max_attempts - 1:
                    print("Transaction non encore validée ou incomplète, attente...")
                    await asyncio.sleep(2)
            
            # Si on a épuisé toutes les tentatives
            error_message = "Transaction non validée après plusieurs tentatives"
            if hasattr(response, 'error'):
                error_message = response.error.get("message", error_message)
            
            return {
                "status": "error",
                "message": error_message
            }
            
        except Exception as e:
            print(f"Erreur XRPL détaillée: {type(e).__name__} - {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    async def check_balance(self, address: str) -> float:
        """Vérifie le solde d'un compte XRPL."""
        try:
            response = await asyncio.to_thread(
                self.client.request,
                {
                    "command": "account_info",
                    "account": address,
                    "ledger_index": "validated"
                }
            )
            
            if "result" in response:
                balance = float(response["result"]["account_data"]["Balance"]) / 1000000
                return balance
            return 0.0
        except Exception:
            return 0.0

xrpl_service = XRPLService() 