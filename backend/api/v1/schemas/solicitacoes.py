"""
Schemas Pydantic para Solicitações de Orçamento
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ============= SCHEMAS PARA SOLICITAÇÃO =============

class SolicitacaoBase(BaseModel):
    categoria: str
    descricao: str
    localizacao: str
    prazo_desejado: Optional[str] = None
    informacoes_adicionais: Optional[str] = None

class SolicitacaoCreate(SolicitacaoBase):
    pass

class SolicitacaoUpdate(BaseModel):
    categoria: Optional[str] = None
    descricao: Optional[str] = None
    localizacao: Optional[str] = None
    prazo_desejado: Optional[str] = None
    informacoes_adicionais: Optional[str] = None
    status: Optional[str] = None

class SolicitacaoResponse(SolicitacaoBase):
    id: int
    cliente_id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    # Dados do cliente
    cliente_nome: Optional[str] = None
    cliente_avaliacao: Optional[float] = None
    
    # Contagem de orçamentos
    quantidade_orcamentos: Optional[int] = None

    class Config:
        from_attributes = True

# ============= SCHEMA PARA LISTAGEM DO PRESTADOR =============

class SolicitacaoDisponivel(BaseModel):
    """Solicitações disponíveis para o prestador responder"""
    id: int
    categoria: str
    descricao: str
    localizacao: str
    prazo_desejado: Optional[str] = None
    created_at: datetime
    cliente_nome: str
    cliente_avaliacao: float
    quantidade_orcamentos: int

    class Config:
        from_attributes = True

