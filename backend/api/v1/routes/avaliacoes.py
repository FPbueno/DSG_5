"""
Rotas de Avaliações (modo memória)
"""
from fastapi import APIRouter, status, HTTPException
from ..schemas import AvaliacaoCreate, AvaliacaoResponse, MediaPrestadorResponse
from typing import Dict, Any, List
from datetime import datetime


router = APIRouter(prefix="/avaliacoes", tags=["avaliacoes"])

_avaliacoes: Dict[int, Dict[str, Any]] = {}
_seq_av = iter(range(1, 10_000_000))


@router.post("/", response_model=AvaliacaoResponse, status_code=status.HTTP_201_CREATED)
def criar(data: AvaliacaoCreate):
    # Impede duplicidade por orçamento
    if any(a for a in _avaliacoes.values() if a["orcamento_id"] == data.orcamento_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Avaliação já existe para este orçamento"
        )
    aid = next(_seq_av)
    now = datetime.utcnow()
    av = {
        "id": aid,
        "orcamento_id": data.orcamento_id,
        "cliente_id": data.cliente_id,
        "prestador_id": data.prestador_id,
        "estrelas": data.estrelas,
        "comentario": data.comentario,
        "created_at": now,
    }
    _avaliacoes[aid] = av
    return AvaliacaoResponse(id=aid, estrelas=data.estrelas, comentario=data.comentario, created_at=now)


@router.get("/media/{prestador_id}", response_model=MediaPrestadorResponse)
def media(prestador_id: int):
    notas = [a["estrelas"] for a in _avaliacoes.values() if a["prestador_id"] == prestador_id]
    if not notas:
        return MediaPrestadorResponse(prestador_id=prestador_id, media=0.0, total=0)
    media_valor = sum(notas) / len(notas)
    return MediaPrestadorResponse(prestador_id=prestador_id, media=media_valor, total=len(notas))

