import os
from dotenv import load_dotenv

# 1. Load the .env file
load_dotenv()

# 2. Read variables
STORAGE_MODE = os.getenv("STORAGE_MODE", "local")

# Azure Config
AZURE_CONN_STRING = os.getenv("AZURE_CONN_STRING")
CONTAINER_NAME = os.getenv("AZURE_CONTAINER_NAME", "videos")

# Local Config
BASE_URL = "http://127.0.0.1:8000"
UPLOAD_DIR = "static"

# Security Config (Now loaded from .env for safety)
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))