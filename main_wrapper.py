"""
Production wrapper for main.py
Imports the original main.py and adds demo mode functionality
This file is used ONLY for Railway deployment
"""
import os
import sys
from pathlib import Path

# Import configuration
from config import DEMO_MODE, PORT, ALLOWED_ORIGINS, APP_NAME, APP_VERSION

# Import original main.py
from main import app, mongo_client, db, logger

# Import custom middleware and routes
from middleware.demo_middleware import DemoModeMiddleware
from routes.health_routes import router as health_router, init_health_routes

# Apply demo mode middleware if enabled
if DEMO_MODE:
    app.add_middleware(DemoModeMiddleware, demo_mode=True)
    logger.info("🎭 DEMO MODE ENABLED - Read-only mode active")

# Initialize and add health check routes
init_health_routes(mongo_client, DEMO_MODE, APP_NAME, APP_VERSION)
app.include_router(health_router, tags=["Health"])

# Update CORS if needed
from fastapi.middleware.cors import CORSMiddleware

# Remove default CORS (if any) and add custom
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info(f"CORS configured for: {ALLOWED_ORIGINS}")

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting server on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
