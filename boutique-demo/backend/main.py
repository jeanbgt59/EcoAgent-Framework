#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="EcoAgent Application",
    description="Application générée par EcoAgent Framework",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "🚀 EcoAgent Application API",
        "status": "active",
        "framework": "EcoAgent v2.0"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "ecoagent-app"}

if __name__ == "__main__":
    print("🚀 Démarrage EcoAgent Application")
    print("📡 API disponible sur: http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
