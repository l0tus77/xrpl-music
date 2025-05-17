from fastapi import FastAPI
from src.routes import auth, user

app = FastAPI(title="XRPL Auction API")

# Inclure les routers
app.include_router(auth.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Welcome to XRPL Auction API"} 