"""
Schemas Pydantic para Avaliações
"""
from pydantic import BaseModel, conint
from typing import Optional
from datetime import datetime


class AvaliacaoBase(BaseModel):
    estrelas: conint(ge=1, le=5)
    comentario: Optional[str] = None


class AvaliacaoCreate(AvaliacaoBase):
    orcamento_id: int
    cliente_id: int
    prestador_id: int


class AvaliacaoResponse(AvaliacaoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MediaPrestadorResponse(BaseModel):
    prestador_id: int
    media: float
    total: int


