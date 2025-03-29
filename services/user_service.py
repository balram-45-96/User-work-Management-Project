from database import users_collection
from models.user import User
from utils.auth import hash_password, verify_password, create_access_token
from bson import ObjectId

async def create_user(user: User):
    user.password = hash_password(user.password)
    user_dict = user.dict()
    result = await users_collection.insert_one(user_dict)
    return {**user_dict, "id": str(result.inserted_id)}

async def authenticate_user(email: str, password: str):
    user = await users_collection.find_one({"email": email})
    if user:
        if verify_password(password, user["password"]):
            print("User data:", user['_id'])
            access_token = create_access_token(data={"email": user["email"], "id": str(user['_id'])})
            return access_token
    return None
