"""
Serviço de Solicitações de Orçamento
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.db_models import Solicitacao, Cliente, StatusSolicitacao
from ..schemas import SolicitacaoCreate, SolicitacaoUpdate

def criar_solicitacao(
    db: Session,
    cliente_id: int,
    solicitacao_data: SolicitacaoCreate
) -> Solicitacao:
    """Cliente cria nova solicitação de orçamento"""
    solicitacao = Solicitacao(
        cliente_id=cliente_id,
        categoria=solicitacao_data.categoria,
        descricao=solicitacao_data.descricao,
        localizacao=solicitacao_data.localizacao,
        prazo_desejado=solicitacao_data.prazo_desejado,
        informacoes_adicionais=solicitacao_data.informacoes_adicionais,
        status=StatusSolicitacao.AGUARDANDO
    )
    db.add(solicitacao)
    db.commit()
    db.refresh(solicitacao)
    return solicitacao

def listar_solicitacoes_cliente(db: Session, cliente_id: int) -> List[Solicitacao]:
    """Lista todas solicitações de um cliente"""
    return db.query(Solicitacao).filter(
        Solicitacao.cliente_id == cliente_id
    ).order_by(Solicitacao.created_at.desc()).all()

def buscar_solicitacao_por_id(db: Session, solicitacao_id: int) -> Optional[Solicitacao]:
    """Busca solicitação por ID"""
    return db.query(Solicitacao).filter(Solicitacao.id == solicitacao_id).first()

def listar_solicitacoes_disponiveis(
    db: Session,
    categorias_prestador: List[str]
) -> List[Solicitacao]:
    """
    Lista solicitações disponíveis para prestador responder
    Filtra por categoria e status
    """
    todas_solicitacoes = db.query(Solicitacao).filter(
        Solicitacao.status.in_([
            StatusSolicitacao.AGUARDANDO,
            StatusSolicitacao.COM_ORCAMENTOS
        ])
    ).all()
    
    print(f"Total solicitações abertas: {len(todas_solicitacoes)}")
    for sol in todas_solicitacoes:
        print(f"Solicitação ID {sol.id}: categoria='{sol.categoria}'")
    
    return db.query(Solicitacao).filter(
        Solicitacao.categoria.in_(categorias_prestador),
        Solicitacao.status.in_([
            StatusSolicitacao.AGUARDANDO,
            StatusSolicitacao.COM_ORCAMENTOS
        ])
    ).order_by(Solicitacao.created_at.desc()).all()

def atualizar_status_solicitacao(
    db: Session,
    solicitacao_id: int,
    novo_status: StatusSolicitacao
) -> Optional[Solicitacao]:
    """Atualiza status da solicitação"""
    solicitacao = buscar_solicitacao_por_id(db, solicitacao_id)
    if solicitacao:
        solicitacao.status = novo_status
        db.commit()
        db.refresh(solicitacao)
    return solicitacao

def cancelar_solicitacao(db: Session, solicitacao_id: int, cliente_id: int) -> bool:
    """Cliente cancela sua solicitação"""
    solicitacao = buscar_solicitacao_por_id(db, solicitacao_id)
    if not solicitacao or solicitacao.cliente_id != cliente_id:
        return False
    
    solicitacao.status = StatusSolicitacao.CANCELADA
    db.commit()
    return True

def deletar_solicitacao(db: Session, solicitacao_id: int, cliente_id: int) -> bool:
    """
    Cliente deleta sua solicitação
    Só pode deletar se não houver orçamentos aceitos
    """
    from fastapi import HTTPException
    from ..models.db_models import Orcamento, StatusOrcamento
    
    solicitacao = buscar_solicitacao_por_id(db, solicitacao_id)
    if not solicitacao:
        return False
    
    # Verifica se é o dono da solicitação
    if solicitacao.cliente_id != cliente_id:
        raise HTTPException(status_code=403, detail="Não autorizado")
    
    # Verifica se há orçamentos aceitos
    orcamento_aceito = db.query(Orcamento).filter(
        Orcamento.solicitacao_id == solicitacao_id,
        Orcamento.status == StatusOrcamento.ACEITO
    ).first()
    
    if orcamento_aceito:
        raise HTTPException(
            status_code=400,
            detail="Não é possível deletar solicitação com orçamento aceito"
        )
    
    # Deleta todos os orçamentos associados primeiro
    db.query(Orcamento).filter(
        Orcamento.solicitacao_id == solicitacao_id
    ).delete()
    
    # Deleta a solicitação
    db.delete(solicitacao)
    db.commit()
    return True

