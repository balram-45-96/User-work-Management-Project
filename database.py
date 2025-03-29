from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DETAILS

client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.test  # Database ka naam
tasks_collection = database.get_collection("tasks")  # Collection ka naam 

users_collection = database.get_collection("users")  # ✅ Ensure this is defined