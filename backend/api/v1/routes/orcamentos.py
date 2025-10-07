"""
Rotas de Orçamentos
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..schemas import (
    OrcamentoCreate, OrcamentoResponse,
    OrcamentoComLimites, CalcularLimitesRequest, CalcularLimitesResponse
)
from ..services.orcamento_service import (
    criar_orcamento, listar_orcamentos_solicitacao,
    listar_orcamentos_prestador, aceitar_orcamento, marcar_realizado,
    deletar_orcamento
)
from ..services.solicitacao_service import buscar_solicitacao_por_id
from ..services.ml_service import calcular_limites_preco

router = APIRouter(prefix="/orcamentos")

# ============= PRESTADOR =============

@router.get("/calcular-limites/{solicitacao_id}", response_model=CalcularLimitesResponse)
def calcular_limites_endpoint(
    solicitacao_id: int,
    db: Session = Depends(get_db)
):
    """
    Calcula limites de preço (mínimo, sugerido, máximo) para uma solicitação
    Apenas para prestador usar como referência
    """
    solicitacao = buscar_solicitacao_por_id(db, solicitacao_id)
    if not solicitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitação não encontrada"
        )
    
    # Calcula limites usando ML
    limites = calcular_limites_preco(
        categoria=solicitacao.categoria,
        descricao=solicitacao.descricao,
        localizacao=solicitacao.localizacao
    )
    
    return limites

@router.post("/criar", response_model=OrcamentoResponse, status_code=status.HTTP_201_CREATED)
def criar_orcamento_endpoint(
    orcamento_data: OrcamentoCreate,
    prestador_id: int = Query(...),  # TODO: Extrair do token JWT
    db: Session = Depends(get_db)
):
    """Prestador cria orçamento para uma solicitação"""
    # Busca solicitação
    solicitacao = buscar_solicitacao_por_id(db, orcamento_data.solicitacao_id)
    if not solicitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitação não encontrada"
        )
    
    # Calcula limites do ML para validação
    limites = calcular_limites_preco(
        categoria=solicitacao.categoria,
        descricao=solicitacao.descricao,
        localizacao=solicitacao.localizacao
    )
    
    # Cria orçamento (valida limites internamente)
    orcamento = criar_orcamento(db, prestador_id, orcamento_data, limites)
    
    return {
        **orcamento.__dict__,
        "status": orcamento.status.value,
        "prestador_nome": orcamento.prestador.nome,
        "prestador_avaliacao": orcamento.prestador.avaliacao_media
    }

@router.put("/{orcamento_id}/realizado", response_model=OrcamentoResponse)
def marcar_realizado_endpoint(
    orcamento_id: int,
    prestador_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Prestador marca orçamento como realizado (serviço concluído)."""
    orc = marcar_realizado(db, orcamento_id, prestador_id)
    if not orc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orçamento não encontrado"
        )
    return {
        **orc.__dict__,
        "status": orc.status.value,
        "prestador_nome": orc.prestador.nome,
        "prestador_avaliacao": orc.prestador.avaliacao_media
    }

@router.get("/meus-orcamentos", response_model=List[OrcamentoComLimites])
def listar_meus_orcamentos(
    prestador_id: int = Query(...),  # TODO: Extrair do token JWT
    db: Session = Depends(get_db)
):
    """Prestador lista seus orçamentos enviados"""
    orcamentos = listar_orcamentos_prestador(db, prestador_id)
    
    resultado = []
    for orc in orcamentos:
        resultado.append({
            "id": orc.id,
            "solicitacao_id": orc.solicitacao_id,
            "prestador_id": orc.prestador_id,
            "valor_ml_minimo": orc.valor_ml_minimo,
            "valor_ml_sugerido": orc.valor_ml_sugerido,
            "valor_ml_maximo": orc.valor_ml_maximo,
            "valor_proposto": orc.valor_proposto,
            "prazo_execucao": orc.prazo_execucao,
            "observacoes": orc.observacoes,
            "condicoes": orc.condicoes,
            "status": orc.status.value,
            "created_at": orc.created_at,
            "prestador_nome": orc.prestador.nome,
            "prestador_avaliacao": orc.prestador.avaliacao_media,
            "categoria": orc.solicitacao.categoria,
            "descricao": orc.solicitacao.descricao
        })
    
    return resultado

@router.delete("/{orcamento_id}")
def deletar_orcamento_endpoint(
    orcamento_id: int,
    prestador_id: int = Query(...),  # TODO: Extrair do token JWT
    db: Session = Depends(get_db)
):
    """Prestador deleta um orçamento (apenas status AGUARDANDO)"""
    sucesso = deletar_orcamento(db, orcamento_id, prestador_id)
    
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orçamento não encontrado"
        )
    
    return {"message": "Orçamento deletado com sucesso"}

# ============= CLIENTE =============

@router.get("/solicitacao/{solicitacao_id}", response_model=List[OrcamentoResponse])
def listar_orcamentos_da_solicitacao(
    solicitacao_id: int,
    cliente_id: int = Query(...),  # TODO: Extrair do token JWT
    db: Session = Depends(get_db)
):
    """Cliente lista orçamentos recebidos para sua solicitação"""
    # Verifica se solicitação existe e pertence ao cliente
    solicitacao = buscar_solicitacao_por_id(db, solicitacao_id)
    if not solicitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitação não encontrada"
        )
    
    if solicitacao.cliente_id != cliente_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado"
        )
    
    orcamentos = listar_orcamentos_solicitacao(db, solicitacao_id)
    
    # Formata resposta (SEM os limites do ML)
    from ..models.db_models import Avaliacao
    
    resultado = []
    for orc in orcamentos:
        # Verifica se já foi avaliado
        ja_avaliado = db.query(Avaliacao).filter(
            Avaliacao.orcamento_id == orc.id
        ).first() is not None
        
        resultado.append({
            "id": orc.id,
            "solicitacao_id": orc.solicitacao_id,
            "prestador_id": orc.prestador_id,
            "valor_proposto": orc.valor_proposto,
            "prazo_execucao": orc.prazo_execucao,
            "observacoes": orc.observacoes,
            "condicoes": orc.condicoes,
            "status": orc.status.value,
            "created_at": orc.created_at,
            "prestador_nome": orc.prestador.nome,
            "prestador_avaliacao": orc.prestador.avaliacao_media,
            "ja_avaliado": ja_avaliado
        })
    
    return resultado

@router.put("/{orcamento_id}/aceitar", response_model=OrcamentoResponse)
def aceitar_orcamento_endpoint(
    orcamento_id: int,
    cliente_id: int = Query(...),  # TODO: Extrair do token JWT
    db: Session = Depends(get_db)
):
    """Cliente aceita um orçamento"""
    orcamento = aceitar_orcamento(db, orcamento_id, cliente_id)
    
    if not orcamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orçamento não encontrado"
        )
    
    return {
        **orcamento.__dict__,
        "status": orcamento.status.value,
        "prestador_nome": orcamento.prestador.nome,
        "prestador_avaliacao": orcamento.prestador.avaliacao_media
    }

@router.get("/cliente/{cliente_id}/realizados", response_model=List[OrcamentoResponse])
def listar_orcamentos_realizados_cliente(
    cliente_id: int,
    db: Session = Depends(get_db)
):
    """Cliente lista orçamentos realizados para avaliação"""
    from ..models.db_models import Orcamento, Solicitacao, Prestador, StatusOrcamento, Avaliacao
    
    orcamentos = db.query(Orcamento).join(
        Solicitacao, Orcamento.solicitacao_id == Solicitacao.id
    ).join(
        Prestador, Orcamento.prestador_id == Prestador.id
    ).filter(
        Solicitacao.cliente_id == cliente_id,
        Orcamento.status == StatusOrcamento.REALIZADO
    ).all()
    
    resultado = []
    for orc in orcamentos:
        # Verifica se já foi avaliado
        ja_avaliado = db.query(Avaliacao).filter(
            Avaliacao.orcamento_id == orc.id
        ).first() is not None
        
        resultado.append({
            "id": orc.id,
            "solicitacao_id": orc.solicitacao_id,
            "prestador_id": orc.prestador_id,
            "valor_proposto": orc.valor_proposto,
            "prazo_execucao": orc.prazo_execucao,
            "observacoes": orc.observacoes,
            "condicoes": orc.condicoes,
            "status": orc.status.value,
            "created_at": orc.created_at,
            "prestador_nome": orc.prestador.nome,
            "prestador_avaliacao": orc.prestador.avaliacao_media,
            "ja_avaliado": ja_avaliado
        })
    
    return resultado

