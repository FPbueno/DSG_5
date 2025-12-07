"""
Rotas de Orçamentos (modo memória)
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict, Any, Optional
from datetime import datetime
from ..schemas import (
    OrcamentoCreate, OrcamentoResponse,
    OrcamentoComLimites, CalcularLimitesRequest, CalcularLimitesResponse
)
from ..services.ml_service import calcular_limites_preco
from .solicitacoes import _buscar_solicitacao_por_id
from .usuarios import _buscar_prestador_por_id

router = APIRouter(prefix="/orcamentos")

# Armazenamento em memória
_orcamentos: Dict[int, Dict[str, Any]] = {}
_seq_orc = iter(range(1, 10_000_000))

# Helpers
def _novo_orcamento(prestador_id: int, solicitacao_id: int, data: OrcamentoCreate, limites: Dict[str, Any]) -> Dict[str, Any]:
    oid = next(_seq_orc)
    now = datetime.utcnow()
    orc = {
        "id": oid,
        "solicitacao_id": solicitacao_id,
        "prestador_id": prestador_id,
        "valor_ml_minimo": limites.get("valor_minimo"),
        "valor_ml_sugerido": limites.get("valor_sugerido"),
        "valor_ml_maximo": limites.get("valor_maximo"),
        "valor_proposto": data.valor_proposto,
        "prazo_execucao": data.prazo_execucao,
        "observacoes": data.observacoes,
        "condicoes": data.condicoes,
        "datetime_inicio": data.datetime_inicio,
        "datetime_fim": data.datetime_fim,
        "status": "aguardando",
        "created_at": now,
        "realizado": False,
    }
    _orcamentos[oid] = orc
    return orc

def _listar_orcamentos_prestador(pid: int) -> List[Dict[str, Any]]:
    return [o for o in _orcamentos.values() if o["prestador_id"] == pid]

def _listar_orcamentos_solicitacao(sid: int) -> List[Dict[str, Any]]:
    return [o for o in _orcamentos.values() if o["solicitacao_id"] == sid]

def _buscar_orcamento(oid: int) -> Optional[Dict[str, Any]]:
    return _orcamentos.get(oid)

def _deletar_orcamento(oid: int, prestador_id: int) -> bool:
    orc = _orcamentos.get(oid)
    if not orc or orc["prestador_id"] != prestador_id or orc["status"] != "aguardando":
        return False
    _orcamentos.pop(oid, None)
    return True

def _aceitar_orcamento(oid: int, cliente_id: int) -> Optional[Dict[str, Any]]:
    orc = _orcamentos.get(oid)
    if not orc:
        return None
    sol = _buscar_solicitacao_por_id(orc["solicitacao_id"])
    if not sol or sol["cliente_id"] != cliente_id:
        return None
    orc["status"] = "aceito"
    orc["updated_at"] = datetime.utcnow()
    return orc

def _marcar_realizado(oid: int, prestador_id: int) -> Optional[Dict[str, Any]]:
    orc = _orcamentos.get(oid)
    if not orc or orc["prestador_id"] != prestador_id:
        return None
    orc["status"] = "realizado"
    orc["realizado"] = True
    orc["datetime_fim"] = datetime.utcnow()
    return orc

# ============= PRESTADOR =============

@router.get("/calcular-limites/{solicitacao_id}", response_model=CalcularLimitesResponse)
def calcular_limites_endpoint(
    solicitacao_id: int,
):
    """
    Calcula limites de preço (mínimo, sugerido, máximo) para uma solicitação
    Apenas para prestador usar como referência
    """
    solicitacao = _buscar_solicitacao_por_id(solicitacao_id)
    if not solicitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitação não encontrada"
        )
    
    # Calcula limites usando ML
    limites = calcular_limites_preco(
        categoria=solicitacao['categoria'],
        descricao=solicitacao['descricao'],
        localizacao=solicitacao['localizacao']
    )
    
    return limites

@router.post("/criar", response_model=OrcamentoResponse, status_code=status.HTTP_201_CREATED)
def criar_orcamento_endpoint(
    orcamento_data: OrcamentoCreate,
    prestador_id: int = Query(...),  # TODO: Extrair do token JWT
):
    """Prestador cria orçamento para uma solicitação"""
    # Busca solicitação
    solicitacao = _buscar_solicitacao_por_id(orcamento_data.solicitacao_id)
    if not solicitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitação não encontrada"
        )
    
    # Calcula limites do ML para validação
    limites = calcular_limites_preco(
        categoria=solicitacao['categoria'],
        descricao=solicitacao['descricao'],
        localizacao=solicitacao['localizacao']
    )
    
    # Cria orçamento com limites ML
    orcamento = _novo_orcamento(prestador_id, orcamento_data.solicitacao_id, orcamento_data, {
        "valor_minimo": limites.valor_minimo if hasattr(limites, "valor_minimo") else limites["valor_minimo"],
        "valor_sugerido": limites.valor_sugerido if hasattr(limites, "valor_sugerido") else limites["valor_sugerido"],
        "valor_maximo": limites.valor_maximo if hasattr(limites, "valor_maximo") else limites["valor_maximo"],
    })
    
    return {
        **orcamento,
        "prestador_nome": "N/A",  # TODO: Implementar join com prestadores
        "prestador_avaliacao": 0.0
    }

@router.put("/{orcamento_id}/realizado", response_model=OrcamentoResponse)
def marcar_realizado_endpoint(
    orcamento_id: int,
    prestador_id: int = Query(...),
):
    """Prestador marca orçamento como realizado (serviço concluído)."""
    orc = _marcar_realizado(orcamento_id, prestador_id)
    if not orc or not orc.get('id'):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orçamento não encontrado"
        )
    return {
        **orc,
        "prestador_nome": "N/A",  # TODO: Implementar join com prestadores
        "prestador_avaliacao": 0.0
    }

@router.get("/meus-orcamentos", response_model=List[OrcamentoComLimites])
def listar_meus_orcamentos(
    prestador_id: int = Query(...),  # TODO: Extrair do token JWT
):
    """Prestador lista seus orçamentos enviados"""
    orcamentos = _listar_orcamentos_prestador(prestador_id)
    
    resultado = []
    for orc in orcamentos:
        resultado.append({
            "id": orc['id'],
            "solicitacao_id": orc['solicitacao_id'],
            "prestador_id": orc['prestador_id'],
            "valor_ml_minimo": orc['valor_ml_minimo'],
            "valor_ml_sugerido": orc['valor_ml_sugerido'],
            "valor_ml_maximo": orc['valor_ml_maximo'],
            "valor_proposto": orc['valor_proposto'],
            "prazo_execucao": orc['prazo_execucao'],
            "observacoes": orc['observacoes'],
            "condicoes": orc['condicoes'],
            "status": orc['status'],
            "created_at": orc['created_at'],
            "datetime_inicio": orc.get('datetime_inicio'),
            "datetime_fim": orc.get('datetime_fim'),
            "prestador_nome": orc.get('prestadores', {}).get('nome', 'N/A'),
            "prestador_avaliacao": orc.get('prestadores', {}).get('avaliacao_media', 0.0),
            "categoria": orc.get('solicitacoes', {}).get('categoria', 'N/A'),
            "descricao": orc.get('solicitacoes', {}).get('descricao', 'N/A')
        })
    
    return resultado

@router.delete("/{orcamento_id}")
def deletar_orcamento_endpoint(
    orcamento_id: int,
    prestador_id: int = Query(...),  # TODO: Extrair do token JWT
):
    """Prestador deleta um orçamento (apenas status AGUARDANDO)"""
    sucesso = _deletar_orcamento(orcamento_id, prestador_id)
    
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
):
    """Cliente lista orçamentos recebidos para sua solicitação"""
    # Verifica se solicitação existe e pertence ao cliente
    solicitacao = _buscar_solicitacao_por_id(solicitacao_id)
    if not solicitacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitação não encontrada"
        )
    
    if solicitacao['cliente_id'] != cliente_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não autorizado"
        )
    
    orcamentos = _listar_orcamentos_solicitacao(solicitacao_id)
    
    # Formata resposta (SEM os limites do ML)
    resultado = []
    for orc in orcamentos:
        resultado.append({
            "id": orc['id'],
            "solicitacao_id": orc['solicitacao_id'],
            "prestador_id": orc['prestador_id'],
            "valor_proposto": orc['valor_proposto'],
            "prazo_execucao": orc['prazo_execucao'],
            "observacoes": orc['observacoes'],
            "condicoes": orc['condicoes'],
            "status": orc['status'],
            "created_at": orc['created_at'],
            "prestador_nome": orc.get('prestadores', {}).get('nome', 'N/A'),
            "prestador_avaliacao": orc.get('prestadores', {}).get('avaliacao_media', 0.0),
            "ja_avaliado": False
        })
    
    return resultado

@router.put("/{orcamento_id}/aceitar", response_model=OrcamentoResponse)
def aceitar_orcamento_endpoint(
    orcamento_id: int,
    cliente_id: int = Query(...),  # TODO: Extrair do token JWT
):
    """Cliente aceita um orçamento"""
    orcamento = _aceitar_orcamento(orcamento_id, cliente_id)
    
    if not orcamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orçamento não encontrado"
        )
    
    return {
        **orcamento,
        "prestador_nome": "N/A",  # TODO: Implementar join com prestadores
        "prestador_avaliacao": 0.0
    }

@router.get("/cliente/{cliente_id}/realizados", response_model=List[OrcamentoResponse])
def listar_orcamentos_realizados_cliente(
    cliente_id: int,
):
    """Cliente lista orçamentos realizados para avaliação"""
    resultado = []
    for orc in _orcamentos.values():
        sol = _buscar_solicitacao_por_id(orc["solicitacao_id"])
        if orc.get("status") == "realizado" and sol and sol["cliente_id"] == cliente_id:
            resultado.append({
                "id": orc['id'],
                "solicitacao_id": orc['solicitacao_id'],
                "prestador_id": orc['prestador_id'],
                "valor_proposto": orc['valor_proposto'],
                "prazo_execucao": orc['prazo_execucao'],
                "observacoes": orc['observacoes'],
                "condicoes": orc['condicoes'],
                "status": orc['status'],
                "created_at": orc['created_at'],
                "realizado": True,
                "prestador_nome": "N/A",
                "prestador_avaliacao": 0.0,
                "ja_avaliado": False
            })
    return resultado
