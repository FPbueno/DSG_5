# Routes Package
from fastapi import APIRouter
from .auth import router as auth_router
from .clients import router as clients_router
from .services import router as services_router
from .quotes import router as quotes_router
from .ml import router as ml_router
from .analytics import router as analytics_router

# Novas rotas do marketplace
from .usuarios import router as usuarios_router
from .solicitacoes import router as solicitacoes_router
from .orcamentos import router as orcamentos_router
from .avaliacoes import router as avaliacoes_router

# Router principal que combina todas as rotas
router = APIRouter()

# Rotas antigas (manter compatibilidade)
router.include_router(auth_router, tags=["authentication"])
router.include_router(clients_router, tags=["clients"])
router.include_router(services_router, tags=["services"])
router.include_router(quotes_router, tags=["quotes"])
router.include_router(ml_router, tags=["ml"])
router.include_router(analytics_router, tags=["analytics"])

# Novas rotas do marketplace
router.include_router(usuarios_router, tags=["usuarios"])
router.include_router(solicitacoes_router, tags=["solicitacoes"])
router.include_router(orcamentos_router, tags=["orcamentos"])
router.include_router(avaliacoes_router)

__all__ = ["router"]