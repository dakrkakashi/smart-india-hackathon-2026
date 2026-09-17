"""
FastAPI Application Entry Point
Main application setup with routers, middleware, and lifecycle events
"""

import sys
import os

# Ensure backend and pralay root are in sys.path
_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
_BACKEND_DIR = os.path.abspath(os.path.join(_CURRENT_DIR, ".."))
_PRALAY_DIR = os.path.abspath(os.path.join(_CURRENT_DIR, "..", ".."))

for path in [_PRALAY_DIR, _BACKEND_DIR]:
    if path not in sys.path:
        sys.path.insert(0, path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db, close_db
from app.api.v1.router import api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events - startup and shutdown"""
    # Startup
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    try:
        await init_db()
        print("Database initialized")
    except Exception as e:
        print(f"Database initialization deferred: {e}")

    yield

    # Shutdown
    print("Shutting down application")
    try:
        await close_db()
        print("Database connections closed")
    except Exception as e:
        print(f"Error closing database connections: {e}")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="PRALAYADARSHI - Flash Flood & Compound Risk Prediction System for Hilly Regions (SIH PS 26192)",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - health check"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy",
        "north_star_capabilities": [
            "1. WHERE is the risk? (Hyperlocal village/ward boundaries)",
            "2. HOW SEVERE? (4-Tier GREEN/YELLOW/ORANGE/RED Compound Risk)",
            "3. HOW SOON? (Physics-grounded Estimated Lead Time)",
            "4. WHAT NOW? (Safe shelter assignment & safe evacuation routing)"
        ]
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "engine": "active",
        "alert_fatigue_cooldown_min": 30
    }


# Include V1 API Routers
app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
