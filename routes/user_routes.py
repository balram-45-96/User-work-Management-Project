from fastapi import APIRouter, HTTPException
from models.user import User
from services.user_service import create_user, authenticate_user
from pydantic import BaseModel

router = APIRouter()

# Define the input model for login
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/users", response_model=User, tags=["Auth"])
async def register_user(user: User):
    return await create_user(user)

@router.post("/login", response_model=dict, tags=["Auth"])
async def login(user: LoginRequest):
    token = await authenticate_user(user.email, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
