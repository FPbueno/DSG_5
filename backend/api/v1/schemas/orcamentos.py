"""
Schemas Pydantic para Orçamentos
"""
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

# ============= SCHEMAS PARA ORÇAMENTO =============

class OrcamentoBase(BaseModel):
    valor_proposto: float
    prazo_execucao: str
    observacoes: Optional[str] = None
    condicoes: Optional[str] = None

class OrcamentoCreate(OrcamentoBase):
    solicitacao_id: int
    
    @validator('valor_proposto')
    def validar_valor_positivo(cls, v):
        if v <= 0:
            raise ValueError('Valor proposto deve ser maior que zero')
        return v

class OrcamentoUpdate(BaseModel):
    valor_proposto: Optional[float] = None
    prazo_execucao: Optional[str] = None
    observacoes: Optional[str] = None
    condicoes: Optional[str] = None

class OrcamentoResponse(OrcamentoBase):
    id: int
    solicitacao_id: int
    prestador_id: int
    status: str
    created_at: datetime
    realizado: bool = False
    
    # Dados do prestador (para o cliente ver)
    prestador_nome: Optional[str] = None
    prestador_avaliacao: Optional[float] = None

    class Config:
        from_attributes = True

class OrcamentoComLimites(OrcamentoResponse):
    """Schema com limites do ML - apenas para prestador"""
    valor_ml_minimo: float
    valor_ml_sugerido: float
    valor_ml_maximo: float
    categoria: Optional[str] = None
    descricao: Optional[str] = None

# ============= SCHEMAS PARA CÁLCULO DE LIMITES (ML) =============

class CalcularLimitesRequest(BaseModel):
    categoria: str
    descricao: str
    localizacao: str

class CalcularLimitesResponse(BaseModel):
    valor_minimo: float
    valor_sugerido: float
    valor_maximo: float
    categoria_predita: Optional[str] = None

