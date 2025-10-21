"""
Health check routes for monitoring and Railway deployment
"""
from fastapi import APIRouter
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Global variables (will be set by main.py)
mongo_client = None
DEMO_MODE = False
APP_NAME = "Taste Paradise API"
APP_VERSION = "1.0.0"


def init_health_routes(db_client, demo_mode: bool = False, app_name: str = "API", app_version: str = "1.0"):
    """Initialize health routes with database client and config"""
    global mongo_client, DEMO_MODE, APP_NAME, APP_VERSION
    mongo_client = db_client
    DEMO_MODE = demo_mode
    APP_NAME = app_name
    APP_VERSION = app_version
    logger.info("Health check routes initialized")


@router.get("/")
async def root():
    """Root endpoint - basic app info"""
    return {
        "app": APP_NAME,
        "version": APP_VERSION,
        "status": "healthy",
        "mode": "demo" if DEMO_MODE else "production",
        "message": "🎭 Read-only demo mode active" if DEMO_MODE else "API is running"
    }


@router.get("/health")
async def health_check():
    """
    Detailed health check endpoint
    Used by Railway to monitor app health
    """
    health_data = {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "demo_mode": DEMO_MODE,
        "app": APP_NAME,
        "version": APP_VERSION
    }
    
    # Check database connection
    try:
        if mongo_client:
            await mongo_client.admin.command('ping')
            health_data["database"] = "connected"
        else:
            health_data["database"] = "not initialized"
    except Exception as e:
        health_data["database"] = f"error: {str(e)}"
        health_data["status"] = "degraded"
    
    return health_data


@router.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}
