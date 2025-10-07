"""
Rotas de Avaliações
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..schemas import AvaliacaoCreate, AvaliacaoResponse, MediaPrestadorResponse
from ..services.avaliacao_service import criar_avaliacao, obter_media_prestador


router = APIRouter(prefix="/avaliacoes", tags=["avaliacoes"])


@router.post("/", response_model=AvaliacaoResponse, status_code=status.HTTP_201_CREATED)
def criar(data: AvaliacaoCreate, db: Session = Depends(get_db)):
    return criar_avaliacao(db, data)


@router.get("/media/{prestador_id}", response_model=MediaPrestadorResponse)
def media(prestador_id: int, db: Session = Depends(get_db)):
    media_valor = obter_media_prestador(db, prestador_id)
    # conta total
    from ..models.db_models import Avaliacao
    total = db.query(Avaliacao).filter(Avaliacao.prestador_id == prestador_id).count()
    return MediaPrestadorResponse(prestador_id=prestador_id, media=media_valor, total=total)


