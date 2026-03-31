from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health():
    return {"status": "ok", "service": "geoforest-api", "timestamp": datetime.utcnow().isoformat()}


@router.get("/")
async def root():
    return {
        "service": "Geoforest API",
        "version": "1.0.0",
        "docs": "/docs",
    }
