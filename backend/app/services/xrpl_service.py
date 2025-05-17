from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.transactions import Payment
from xrpl.utils import xrp_to_drops
from xrpl.transaction import submit_and_wait
from ..config import settings

class XRPLService:
    def __init__(self):
        self.client = JsonRpcClient(settings.XRPL_NODE_URL)
        self.hot_wallet = Wallet.from_seed(settings.XRPL_HOT_WALLET_SEED)

    async def send_payment(self, destination: str, amount: float) -> dict:
        """Envoie un paiement en XRP à un destinataire."""
        payment = Payment(
            account=self.hot_wallet.classic_address,
            destination=destination,
            amount=xrp_to_drops(amount)
        )
        
        try:
            response = await submit_and_wait(payment, self.client, self.hot_wallet)
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

    async def check_balance(self, address: str) -> float:
        """Vérifie le solde d'un compte XRPL."""
        response = await self.client.request({
            "command": "account_info",
            "account": address,
            "ledger_index": "validated"
        })
        
        if "result" in response:
            balance = float(response["result"]["account_data"]["Balance"]) / 1000000
            return balance
        return 0.0

xrpl_service = XRPLService() 