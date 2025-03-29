from fastapi import FastAPI, HTTPException
from routes.task_routes import router as task_router
from routes.user_routes import router as user_router
from middlewares.auth_middleware import add_cors_middleware
from database import tasks_collection  # Import the tasks_collection to check connection
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DETAILS

# Customize the FastAPI app instance
app = FastAPI(
    title="User Work Management Project",
    description="This is a sample FastAPI project with Swagger documentation.",
    version="1.0.0",
)

add_cors_middleware(app)

# Function to check database connection
async def check_database_connection():
    client = AsyncIOMotorClient(MONGO_DETAILS)
    try:
        # Attempt to fetch a server status
        await client.admin.command('ping')
        print("Database connection successful.")
    except Exception as e:
        print("Database connection failed:", e)
        raise HTTPException(status_code=500, detail="Database connection failed")

@app.on_event("startup")
async def startup_event():
    await check_database_connection()

app.include_router(task_router)
app.include_router(user_router)

# To run the server, use: uvicorn src.main:app --reload 