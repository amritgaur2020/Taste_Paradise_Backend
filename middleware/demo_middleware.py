"""
Demo Mode Middleware
Intercepts write operations in demo mode and returns fake success responses
"""
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


class DemoModeMiddleware(BaseHTTPMiddleware):
    """
    Middleware to handle demo mode.
    Allows GET requests but blocks POST/PUT/DELETE/PATCH operations.
    """
    
    def __init__(self, app, demo_mode: bool = False):
        super().__init__(app)
        self.demo_mode = demo_mode
        if self.demo_mode:
            logger.info("🎭 Demo Mode Middleware activated")
    
    async def dispatch(self, request, call_next):
        # If not in demo mode, allow everything
        if not self.demo_mode:
            return await call_next(request)
        
        # Allow GET requests (read-only operations)
        if request.method == "GET":
            return await call_next(request)
        
        # Allow essential endpoints
        allowed_paths = [
            "/docs",
            "/openapi.json",
            "/health",
            "/",
            "/redoc"
        ]
        
        if any(request.url.path.startswith(path) for path in allowed_paths):
            return await call_next(request)
        
        # Block write operations in demo mode
        if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            logger.info(f"🎭 Demo mode: Blocked {request.method} request to {request.url.path}")
            
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "message": "🎭 Demo Mode: Changes not saved. Full version available for purchase!",
                    "demo": True,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "contact": "amritgaur2020@gmail.com",
                    "note": "This is a read-only demo. Your changes appear to work but are not persisted."
                }
            )
        
        # For any other method, proceed normally
        return await call_next(request)
