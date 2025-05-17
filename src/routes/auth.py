from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from xumm import XummSdk
import jwt
import os
from dotenv import load_dotenv
import time
from src.db import DatabaseManager

load_dotenv()

XUMM_API_KEY = os.getenv("XUMM_API_KEY")
XUMM_API_SECRET = os.getenv("XUMM_API_SECRET")
JWT_SECRET = os.getenv("JWT_SECRET")

xumm = XummSdk(XUMM_API_KEY, XUMM_API_SECRET)
db = DatabaseManager()
router = APIRouter(prefix="/auth", tags=["auth"])

class AuthInitResponse(BaseModel):
    uuid: str
    next_url: str

class AuthStatusResponse(BaseModel):
    address: str
    jwt: str

@router.post("/xumm/init", response_model=AuthInitResponse)
def init_auth():
    payload = xumm.payload.create({
        "txjson": {
            "TransactionType": "SignIn"
        },
        "custom_meta": {
            "instruction": "Login with XUMM",
            "identifier": "login_" + str(int(time.time()))
        }
    })

    print(payload)

    return {
        "uuid": payload.uuid,
        "next_url": payload.next.always
    }

@router.get("/xumm/status/{uuid}", response_model=AuthStatusResponse)
def check_auth(uuid: str):
    result = xumm.payload.get(uuid)
    if not result.meta.signed:
        raise HTTPException(status_code=403, detail="Not signed yet")

    address = result.response.account
    
    # Créer ou récupérer l'utilisateur dans la base de données
    user = db.get_or_create_user(address)
    print(f"User {user.address} logged in (ID: {user.id})")
    
    token = jwt.encode({
        "sub": address,
        "exp": time.time() + 3600
    }, JWT_SECRET, algorithm="HS256")

    return {
        "address": address,
        "jwt": token
    } 