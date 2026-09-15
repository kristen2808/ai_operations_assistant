from fastapi import APIRouter

from backend.app.routers.health import router as health_router
from backend.app.routers.test import router as test_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(test_router)
