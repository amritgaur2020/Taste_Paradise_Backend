# app.py - FastAPI app setup
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import sys

# Import route modules
from routes import auth, orders, menu, reports, tables, kot

def create_app():
    """Create and configure FastAPI application"""
    
    # Determine app directory
    if getattr(sys, 'frozen', False):
        APP_DIR = Path(sys._MEIPASS)
    else:
        APP_DIR = Path(__file__).parent
    
    STATIC_DIR = APP_DIR / "static"
    
    # Create FastAPI app
    app = FastAPI(
        title="Taste Paradise API",
        description="Restaurant Management System",
        version="1.0.0"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Mount static files
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
    
    # Include routers
    app.include_router(auth.router)
    app.include_router(menu.router)
    app.include_router(orders.router)
    app.include_router(kot.router)
    app.include_router(tables.router)
    app.include_router(reports.router)
    
    return app
