# Routes Package
from fastapi import APIRouter
from .usuarios import router as usuarios_router
from .solicitacoes import router as solicitacoes_router
from .orcamentos import router as orcamentos_router
from .avaliacoes import router as avaliacoes_router

# Router principal que combina todas as rotas
router = APIRouter()

# Rotas ativas no modo memória
router.include_router(usuarios_router, tags=["usuarios"])
router.include_router(solicitacoes_router, tags=["solicitacoes"])
router.include_router(orcamentos_router, tags=["orcamentos"])
router.include_router(avaliacoes_router)

__all__ = ["router"]
