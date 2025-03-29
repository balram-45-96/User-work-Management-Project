import os

MONGO_DETAILS = os.getenv("MONGO_DETAILS", "")  # MongoDB connection string
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # JWT secret key
ALGORITHM = os.getenv("ALGORITHM", "HS256")  # JWT algorithm 