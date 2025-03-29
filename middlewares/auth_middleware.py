from fastapi import Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.auth import decode_access_token

def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Change as per your requirements
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

async def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=403, detail="Token is missing")
    
    try:
        token = token.split(" ")[1]  # Extract token from "Bearer <token>"
        payload = decode_access_token(token)
        return payload
    except Exception:
        raise HTTPException(status_code=403, detail="Token is invalid") 