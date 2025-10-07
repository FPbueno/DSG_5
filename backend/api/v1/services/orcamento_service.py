"""
Serviço de Orçamentos
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.db_models import Orcamento, Solicitacao, StatusOrcamento, StatusSolicitacao
from ..schemas import OrcamentoCreate
from fastapi import HTTPException

def criar_orcamento(
    db: Session,
    prestador_id: int,
    orcamento_data: OrcamentoCreate,
    limites_ml: dict
) -> Orcamento:
    """
    Prestador cria orçamento para uma solicitação
    Valida se o valor está dentro dos limites do ML
    """
    # Validar limites
    valor_proposto = orcamento_data.valor_proposto
    valor_minimo = limites_ml["valor_minimo"]
    valor_maximo = limites_ml["valor_maximo"]
    
    if valor_proposto < valor_minimo:
        raise HTTPException(
            status_code=400,
            detail=f"Valor proposto (R$ {valor_proposto:.2f}) abaixo do mínimo permitido (R$ {valor_minimo:.2f})"
        )
    
    if valor_proposto > valor_maximo:
        raise HTTPException(
            status_code=400,
            detail=f"Valor proposto (R$ {valor_proposto:.2f}) acima do máximo permitido (R$ {valor_maximo:.2f})"
        )
    
    # Criar orçamento
    orcamento = Orcamento(
        solicitacao_id=orcamento_data.solicitacao_id,
        prestador_id=prestador_id,
        valor_ml_minimo=limites_ml["valor_minimo"],
        valor_ml_sugerido=limites_ml["valor_sugerido"],
        valor_ml_maximo=limites_ml["valor_maximo"],
        valor_proposto=valor_proposto,
        prazo_execucao=orcamento_data.prazo_execucao,
        observacoes=orcamento_data.observacoes,
        condicoes=orcamento_data.condicoes,
        status=StatusOrcamento.AGUARDANDO
    )
    
    db.add(orcamento)
    
    # Atualizar status da solicitação
    solicitacao = db.query(Solicitacao).filter(
        Solicitacao.id == orcamento_data.solicitacao_id
    ).first()
    
    if solicitacao and solicitacao.status == StatusSolicitacao.AGUARDANDO:
        solicitacao.status = StatusSolicitacao.COM_ORCAMENTOS
    
    db.commit()
    db.refresh(orcamento)
    return orcamento

def listar_orcamentos_solicitacao(
    db: Session,
    solicitacao_id: int
) -> List[Orcamento]:
    """Lista todos orçamentos de uma solicitação (para o cliente ver)"""
    return db.query(Orcamento).filter(
        Orcamento.solicitacao_id == solicitacao_id
    ).order_by(Orcamento.valor_proposto).all()

def listar_orcamentos_prestador(
    db: Session,
    prestador_id: int
) -> List[Orcamento]:
    """Lista todos orçamentos enviados por um prestador"""
    return db.query(Orcamento).filter(
        Orcamento.prestador_id == prestador_id
    ).order_by(Orcamento.created_at.desc()).all()

def buscar_orcamento_por_id(
    db: Session,
    orcamento_id: int
) -> Optional[Orcamento]:
    """Busca orçamento por ID"""
    return db.query(Orcamento).filter(Orcamento.id == orcamento_id).first()

def aceitar_orcamento(
    db: Session,
    orcamento_id: int,
    cliente_id: int
) -> Optional[Orcamento]:
    """
    Cliente aceita um orçamento
    Recusa automaticamente os demais orçamentos da mesma solicitação
    """
    orcamento = buscar_orcamento_por_id(db, orcamento_id)
    
    if not orcamento:
        return None
    
    # Verifica se o cliente é dono da solicitação
    solicitacao = orcamento.solicitacao
    if solicitacao.cliente_id != cliente_id:
        raise HTTPException(status_code=403, detail="Não autorizado")
    
    # Aceita o orçamento escolhido
    orcamento.status = StatusOrcamento.ACEITO
    
    # Recusa os demais orçamentos
    outros_orcamentos = db.query(Orcamento).filter(
        Orcamento.solicitacao_id == orcamento.solicitacao_id,
        Orcamento.id != orcamento_id
    ).all()
    
    for outro in outros_orcamentos:
        outro.status = StatusOrcamento.RECUSADO
    
    # Atualiza status da solicitação para "com_orcamentos" (aceito)
    solicitacao.status = StatusSolicitacao.COM_ORCAMENTOS
    
    db.commit()
    db.refresh(orcamento)
    return orcamento


def marcar_realizado(
    db: Session,
    orcamento_id: int,
    prestador_id: int
) -> Optional[Orcamento]:
    """Prestador marca o serviço como realizado."""
    orc = buscar_orcamento_por_id(db, orcamento_id)
    if not orc:
        return None
    if orc.prestador_id != prestador_id:
        raise HTTPException(status_code=403, detail="Não autorizado")
    # Só pode marcar realizado se já foi aceito
    if orc.status != StatusOrcamento.ACEITO:
        raise HTTPException(status_code=400, detail="Orçamento precisa estar aceito")
    
    orc.status = StatusOrcamento.REALIZADO
    
    # Fecha a solicitação quando prestador marca como realizado
    orc.solicitacao.status = StatusSolicitacao.FECHADA
    
    db.commit()
    db.refresh(orc)
    return orc


def deletar_orcamento(
    db: Session,
    orcamento_id: int,
    prestador_id: int
) -> bool:
    """
    Prestador deleta um orçamento
    Só pode deletar se estiver em status AGUARDANDO
    """
    orc = buscar_orcamento_por_id(db, orcamento_id)
    if not orc:
        return False
    
    # Verifica se é o dono do orçamento
    if orc.prestador_id != prestador_id:
        raise HTTPException(status_code=403, detail="Não autorizado")
    
    # Só pode deletar se estiver aguardando
    if orc.status != StatusOrcamento.AGUARDANDO:
        raise HTTPException(
            status_code=400,
            detail="Só é possível deletar orçamentos com status 'Aguardando'"
        )
    
    # Deletar orçamento
    db.delete(orc)
    
    # Verificar se ainda há outros orçamentos na solicitação
    solicitacao_id = orc.solicitacao_id
    outros_orcamentos = db.query(Orcamento).filter(
        Orcamento.solicitacao_id == solicitacao_id,
        Orcamento.id != orcamento_id
    ).count()
    
    # Se não há mais orçamentos, volta status da solicitação para AGUARDANDO
    if outros_orcamentos == 0:
        solicitacao = db.query(Solicitacao).filter(
            Solicitacao.id == solicitacao_id
        ).first()
        if solicitacao and solicitacao.status == StatusSolicitacao.COM_ORCAMENTOS:
            solicitacao.status = StatusSolicitacao.AGUARDANDO
    
    db.commit()
    return True