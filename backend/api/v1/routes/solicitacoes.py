"""
Rotas de Solicitações de Orçamento (modo memória)
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..schemas import (
    SolicitacaoCreate, SolicitacaoResponse,
    SolicitacaoDisponivel
)
from .usuarios import _buscar_prestador_por_id  # usar armazenamento em memória dos usuários

router = APIRouter(prefix="/solicitacoes")

# Armazenamento em memória
_solicitacoes: Dict[int, Dict[str, Any]] = {}
_seq_solicitacao = iter(range(1, 10_000_000))

# Helpers
def _nova_solicitacao(cliente_id: int, data: SolicitacaoCreate) -> Dict[str, Any]:
    sid = next(_seq_solicitacao)
    now = datetime.utcnow()
    sol = {
        "id": sid,
        "cliente_id": cliente_id,
        "categoria": data.categoria,
        "descricao": data.descricao,
        "localizacao": data.localizacao,
        "prazo_desejado": data.prazo_desejado,
        "informacoes_adicionais": data.informacoes_adicionais,
        "status": "aguardando_orcamentos",
        "created_at": now,
        "updated_at": now,
    }
    _solicitacoes[sid] = sol
    return sol

def _listar_solicitacoes_cliente(cliente_id: int) -> List[Dict[str, Any]]:
    return [s for s in _solicitacoes.values() if s["cliente_id"] == cliente_id]

def _buscar_solicitacao_por_id(sid: int) -> Optional[Dict[str, Any]]:
    return _solicitacoes.get(sid)

def _listar_disponiveis(categorias: List[str]) -> List[Dict[str, Any]]:
    cats = set(categorias or [])
    return [
        s for s in _solicitacoes.values()
        if s["status"] == "aguardando_orcamentos" and (not cats or s["categoria"] in cats)
    ]

def _cancelar(sid: int, cliente_id: int) -> bool:
    sol = _solicitacoes.get(sid)
    if not sol or sol["cliente_id"] != cliente_id:
        return False
    sol["status"] = "cancelada"
    sol["updated_at"] = datetime.utcnow()
    return True

def _deletar(sid: int, cliente_id: int) -> bool:
    sol = _solicitacoes.get(sid)
    if not sol or sol["cliente_id"] != cliente_id:
        return False
    _solicitacoes.pop(sid, None)
    return True

# ============= ROTAS ESPECÍFICAS (antes das rotas com path params) =============

@router.get("/minhas", response_model=List[SolicitacaoResponse])
def listar_minhas_solicitacoes(
    cliente_id: int = Query(...),  # TODO: Extrair do token JWT
):
    """Cliente lista suas solicitações"""
    solicitacoes = _listar_solicitacoes_cliente(cliente_id)
    
    # Formata resposta para Supabase
    resultado = []
    for sol in solicitacoes:
        sol_dict = {
            "id": sol['id'],
            "cliente_id": sol['cliente_id'],
            "categoria": sol['categoria'],
            "descricao": sol['descricao'],
            "localizacao": sol['localizacao'],
            "prazo_desejado": sol['prazo_desejado'],
            "informacoes_adicionais": sol['informacoes_adicionais'],
            "status": sol['status'],
            "created_at": sol['created_at'],
            "updated_at": sol['updated_at'],
            "quantidade_orcamentos": 0  # TODO: Implementar contagem de orçamentos
        }
        resultado.append(sol_dict)
    
    return resultado

@router.get("/disponiveis", response_model=List[SolicitacaoDisponivel])
def listar_solicitacoes_disponiveis_endpoint(
    prestador_id: int = Query(...),  # TODO: Extrair do token JWT
):
    """
    Prestador lista solicitações disponíveis
    Filtradas por suas categorias de atuação
    """
    prestador = _buscar_prestador_por_id(prestador_id)
    if not prestador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prestador não encontrado"
        )
    
    print(f"Categorias do prestador: {prestador['categorias']}")
    solicitacoes = _listar_disponiveis(prestador.get('categorias') or [])
    print(f"Solicitações encontradas: {len(solicitacoes)}")
    
    # Formata resposta
    resultado = []
    for sol in solicitacoes:
        resultado.append({
            "id": sol['id'],
            "cliente_id": sol['cliente_id'],
            "categoria": sol['categoria'],
            "descricao": sol['descricao'],
            "localizacao": sol['localizacao'],
            "prazo_desejado": sol['prazo_desejado'],
            "informacoes_adicionais": sol['informacoes_adicionais'],
            "status": sol['status'],
            "created_at": sol['created_at'],
            "updated_at": sol['updated_at'],
            "cliente_nome": sol.get('clientes', {}).get('nome', 'N/A'),
            "cliente_avaliacao": sol.get('clientes', {}).get('avaliacao_media', 0.0),
            "quantidade_orcamentos": 0  # TODO: Implementar contagem de orçamentos
        })
    
    return resultado

# ============= CLIENTE =============

@router.post("/criar", response_model=SolicitacaoResponse, status_code=status.HTTP_201_CREATED)
def criar_solicitacao_endpoint(
    solicitacao_data: SolicitacaoCreate,
    cliente_id: int = Query(...),  # TODO: Extrair do token JWT
):
    """Cliente cria nova solicitação de orçamento"""
    solicitacao = _nova_solicitacao(cliente_id, solicitacao_data)
    return solicitacao

@router.get("/{solicitacao_id}", response_model=SolicitacaoResponse)
def buscar_solicitacao(
    solicitacao_id: int,
):
    """Busca solicitação por ID"""
    solicitacao = _buscar_solicitacao_por_id(solicitacao_id)
    if not solicitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitação não encontrada"
        )
    
    return {
        **solicitacao,
        "cliente_nome": "N/A",  # TODO: Implementar join com clientes
        "cliente_avaliacao": 0.0,
        "quantidade_orcamentos": 0  # TODO: Implementar contagem de orçamentos
    }

@router.delete("/{solicitacao_id}/cancelar", status_code=status.HTTP_204_NO_CONTENT)
def cancelar_solicitacao_endpoint(
    solicitacao_id: int,
    cliente_id: int = Query(...),  # TODO: Extrair do token JWT
):
    """Cliente cancela sua solicitação"""
    sucesso = _cancelar(solicitacao_id, cliente_id)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitação não encontrada ou não autorizado"
        )
    return None

@router.delete("/{solicitacao_id}")
def deletar_solicitacao_endpoint(
    solicitacao_id: int,
    cliente_id: int = Query(...),  # TODO: Extrair do token JWT
):
    """Cliente deleta sua solicitação (remove permanentemente)"""
    sucesso = _deletar(solicitacao_id, cliente_id)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitação não encontrada"
        )
    return {"message": "Solicitação deletada com sucesso"}
