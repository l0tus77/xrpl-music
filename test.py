from xrpl.clients import JsonRpcClient
from xrpl.wallet import generate_faucet_wallet, Wallet
from xrpl.models import AccountInfo, Payment, NFTokenMint, AccountSet
from xrpl.transaction import sign_and_submit
import json
import base64

# Connexion au devnet XRPL
client = JsonRpcClient("https://s.altnet.rippletest.net:51234")

privkey = "ED3E7279D0E01BE53A59513CC537E79FFCD5DFA0B09096DA711D1A6EFD17425C13"
pubkey = "ED0E79C65EA6B042B5642BB6E63A3F06D051C71C229E7C9854A80B174BDBCF9EB1"

def setup_account_for_nft():
    try:
        # Création du wallet à partir de la clé privée
        wallet = Wallet(privkey, 0)
        
        # Configuration du compte pour permettre la création de NFTs
        account_set = AccountSet(
            account=wallet.classic_address,
            set_flag=8  # Flag pour activer NFTokenMinter
        )
        
        # Préparation et envoi de la transaction
        response = sign_and_submit(account_set, wallet, client)
        print("\nConfiguration du compte pour NFTs :")
        print(json.dumps(response.result, indent=4))
        
        return response.result
        
    except Exception as e:
        print(f"Erreur lors de la configuration du compte : {str(e)}")
        raise

def create_nft(uri, metadata):
    try:
        # Création du wallet à partir de la clé privée
        wallet = Wallet(privkey, 0)
        
        # Conversion des métadonnées en base64
        metadata_json = json.dumps(metadata)
        metadata_base64 = base64.b64encode(metadata_json.encode()).decode()
        
        # Création de la transaction NFTokenMint
        nft_mint = NFTokenMint(
            account=wallet.classic_address,
            uri=metadata_base64,
            flags=8,  # Flag pour transférable
            nftoken_taxon=0  # Taxon pour catégoriser le NFT
        )
        
        # Préparation et envoi de la transaction
        response = sign_and_submit(nft_mint, wallet, client)
        print("\nNFT créé avec succès :")
        print(json.dumps(response.result, indent=4))
        
        return response.result
        
    except Exception as e:
        print(f"Erreur lors de la création du NFT : {str(e)}")
        raise

def transfer_xrp(destination_address, amount_xrp):
    try:
        # Création du wallet à partir de la clé privée
        wallet = Wallet(privkey, 0)
        
        # Création de la transaction de paiement
        payment = Payment(
            account=wallet.classic_address,
            destination=destination_address,
            amount=str(amount_xrp * 1000000)  # Conversion en drops (1 XRP = 1,000,000 drops)
        )
        
        # Envoi de la transaction
        response = client.request(payment)
        print("\nTransaction envoyée :")
        print(json.dumps(response.result, indent=4))
        
        return response.result
        
    except Exception as e:
        print(f"Erreur lors du transfert : {str(e)}")
        raise

def main():
    try:
        # Vérification du solde
        print("\nVérification du solde...")
        account_info = AccountInfo(
            account="rMXj5xWb44E6hqhY9VxRwSc5iJpeesJ4n8",
            ledger_index="validated",
            strict=True,
        )
        response = client.request(account_info)
        balance = response.result
        print(json.dumps(balance, indent=4))
        
        # Configuration du compte pour NFTs
        setup_account_for_nft()
        
        # Création du NFT
        metadata = {
            "name": "Mon NFT",
            "description": "Description de mon NFT",
            "image": "https://example.com/image.png",
            "attributes": [
                {"trait_type": "Rareté", "value": "Rare"},
                {"trait_type": "Niveau", "value": 1}
            ]
        }
        create_nft("https://example.com/metadata.json", metadata)

    except Exception as e:
        print(f"Erreur dans le programme principal : {str(e)}")
        raise

if __name__ == "__main__":
    main() 
