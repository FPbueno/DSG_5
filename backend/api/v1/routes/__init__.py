# Routes Package
from fastapi import APIRouter
from .auth import router as auth_router
from .clients import router as clients_router
from .services import router as services_router
from .quotes import router as quotes_router
from .ml import router as ml_router
from .analytics import router as analytics_router

# Router principal que combina todas as rotas
router = APIRouter()

# Inclui todas as rotas
router.include_router(auth_router, tags=["authentication"])
router.include_router(clients_router, tags=["clients"])
router.include_router(services_router, tags=["services"])
router.include_router(quotes_router, tags=["quotes"])
router.include_router(ml_router, tags=["ml"])
router.include_router(analytics_router, tags=["analytics"])

__all__ = ["router"]