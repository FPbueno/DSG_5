"""
Serviço de Avaliações
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from ..models.db_models import Avaliacao, Prestador
from ..schemas.avaliacoes import AvaliacaoCreate


def criar_avaliacao(db: Session, data: AvaliacaoCreate) -> Avaliacao:
    from fastapi import HTTPException
    
    # Verifica se já existe avaliação para este orçamento
    avaliacao_existente = db.query(Avaliacao).filter(
        Avaliacao.orcamento_id == data.orcamento_id
    ).first()
    
    if avaliacao_existente:
        raise HTTPException(
            status_code=400,
            detail="Este orçamento já foi avaliado"
        )
    
    avaliacao = Avaliacao(
        orcamento_id=data.orcamento_id,
        cliente_id=data.cliente_id,
        prestador_id=data.prestador_id,
        estrelas=data.estrelas,
        comentario=data.comentario,
    )
    db.add(avaliacao)
    db.commit()
    db.refresh(avaliacao)

    # Atualiza média do prestador
    atualizar_media_prestador(db, data.prestador_id)

    return avaliacao


def atualizar_media_prestador(db: Session, prestador_id: int) -> None:
    media, total = db.query(func.avg(Avaliacao.estrelas), func.count(Avaliacao.id))\
        .filter(Avaliacao.prestador_id == prestador_id).one()
    media = float(media or 0)
    prestador = db.query(Prestador).get(prestador_id)
    if prestador:
        prestador.avaliacao_media = media
        db.commit()


def obter_media_prestador(db: Session, prestador_id: int) -> Optional[float]:
    media = db.query(func.avg(Avaliacao.estrelas))\
        .filter(Avaliacao.prestador_id == prestador_id).scalar()
    return float(media or 0)


