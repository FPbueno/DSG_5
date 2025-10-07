"""
Schemas Package - Modelos Pydantic para validação
"""
from .usuarios import (
    ClienteCreate, ClienteUpdate, ClienteResponse, ClienteLogin,
    PrestadorCreate, PrestadorUpdate, PrestadorResponse, PrestadorLogin,
    LoginRequest, LoginResponse
)
from .solicitacoes import (
    SolicitacaoCreate, SolicitacaoUpdate, SolicitacaoResponse,
    SolicitacaoDisponivel
)
from .orcamentos import (
    OrcamentoCreate, OrcamentoUpdate, OrcamentoResponse,
    OrcamentoComLimites, CalcularLimitesRequest, CalcularLimitesResponse
)
from .avaliacoes import (
    AvaliacaoCreate, AvaliacaoResponse, MediaPrestadorResponse
)

__all__ = [
    # Clientes
    "ClienteCreate", "ClienteUpdate", "ClienteResponse", "ClienteLogin",
    # Prestadores
    "PrestadorCreate", "PrestadorUpdate", "PrestadorResponse", "PrestadorLogin",
    # Login
    "LoginRequest", "LoginResponse",
    # Solicitações
    "SolicitacaoCreate", "SolicitacaoUpdate", "SolicitacaoResponse",
    "SolicitacaoDisponivel",
    # Orçamentos
    "OrcamentoCreate", "OrcamentoUpdate", "OrcamentoResponse",
    "OrcamentoComLimites", "CalcularLimitesRequest", "CalcularLimitesResponse",
    # Avaliações
    "AvaliacaoCreate", "AvaliacaoResponse", "MediaPrestadorResponse"
]

