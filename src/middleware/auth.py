from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
import os
from dotenv import load_dotenv
import time

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
security = HTTPBearer()

class User(BaseModel):
    address: str

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    try:
        token = credentials.credentials
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        address = payload.get("sub")
        if address is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return User(address=address)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token") 