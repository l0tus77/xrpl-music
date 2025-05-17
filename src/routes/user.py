from fastapi import APIRouter, HTTPException, Depends
from src.middleware.auth import get_current_user, User
from src.db import DatabaseManager

router = APIRouter(prefix="/user", tags=["user"])
db = DatabaseManager()

@router.get("/profile")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    user = db.get_user_by_address(current_user.address)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Récupérer les enchères actives de l'utilisateur
    active_auctions = db.get_active_auctions()
    user_auctions = [auction for auction in active_auctions if auction.creator_id == user.id]
    
    # Récupérer les offres actives de l'utilisateur
    user_bids = db.get_user_bids(current_user.address)
    
    return {
        "address": user.address,
        "created_at": user.created_at,
        "active_auctions": len(user_auctions),
        "active_bids": len(user_bids)
    } 