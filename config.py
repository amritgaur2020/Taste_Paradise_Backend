"""
Configuration for Taste Paradise API
Handles environment variables and app settings
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Demo Mode Configuration
DEMO_MODE = os.getenv("DEMO_MODE", "false").lower() == "true"

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")

# Port Configuration
PORT = int(os.getenv("PORT", 8002))

# CORS Configuration
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,https://tasteparadise-4lvntdxbt-amritgaur2020s-projects.vercel.app"
).split(",")

# App Configuration
APP_NAME = "Taste Paradise API"
APP_VERSION = "1.0.0"
CONTACT_EMAIL = "amritgaur2020@gmail.com"

# Railway Detection
IS_RAILWAY = os.getenv("RAILWAY_ENVIRONMENT") is not None

# Print config on startup (only in development)
if not IS_RAILWAY:
    print(f"🔧 Demo Mode: {DEMO_MODE}")
    print(f"🔧 MongoDB URI: {MONGODB_URI}")
    print(f"🔧 Port: {PORT}")
