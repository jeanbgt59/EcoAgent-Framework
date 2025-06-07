"""
Application FastAPI générée par EcoAgent Framework
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn

from app.database import engine, Base
from app.routers import items, users, health
from app.config import settings

# Création des tables
Base.metadata.create_all(bind=engine)

# Instance FastAPI
app = FastAPI(
    title="Application générée par EcoAgent",
    description="API REST générée automatiquement",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(items.router, prefix="/api/v1", tags=["items"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])

@app.get("/")
async def root():
    return {
        "message": "Application générée par EcoAgent Framework",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
