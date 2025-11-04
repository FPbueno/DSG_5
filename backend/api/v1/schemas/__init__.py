"""
Schemas Package - Modelos Pydantic para validação
"""
from .usuarios import (
    ClienteCreate, ClienteUpdate, ClienteResponse, ClienteLogin,
    PrestadorCreate, PrestadorUpdate, PrestadorResponse, PrestadorLogin,
    LoginRequest, LoginResponse, RegistrarClienteResponse,PrestadorRegistroResponse
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
    "ClienteCreate", "ClienteUpdate", "ClienteResponse", "ClienteLogin", "RegistrarClienteResponse"
    # Prestadores
    "PrestadorCreate", "PrestadorUpdate", "PrestadorResponse", "PrestadorLogin","PrestadorRegistroResponse"
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

