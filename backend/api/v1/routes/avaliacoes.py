"""
Rotas de Avaliações
"""
from fastapi import APIRouter, status, HTTPException
from ..schemas import AvaliacaoCreate, AvaliacaoResponse, MediaPrestadorResponse
from ..services.avaliacao_service_supabase import criar_avaliacao, obter_media_prestador, contar_avaliacoes_prestador


router = APIRouter(prefix="/avaliacoes", tags=["avaliacoes"])


@router.post("/", response_model=AvaliacaoResponse, status_code=status.HTTP_201_CREATED)
def criar(data: AvaliacaoCreate):
    resultado = criar_avaliacao(data)
    if not resultado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Avaliação já existe para este orçamento"
        )
    return resultado


@router.get("/media/{prestador_id}", response_model=MediaPrestadorResponse)
def media(prestador_id: int):
    media_valor = obter_media_prestador(prestador_id)
    total = contar_avaliacoes_prestador(prestador_id)
    return MediaPrestadorResponse(prestador_id=prestador_id, media=media_valor, total=total)


