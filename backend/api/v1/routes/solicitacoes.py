"""
Rotas de Solicitações de Orçamento
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from ..schemas import (
    SolicitacaoCreate, SolicitacaoResponse,
    SolicitacaoDisponivel
)
from ..services.solicitacao_service_supabase import (
    criar_solicitacao, listar_solicitacoes_cliente,
    buscar_solicitacao_por_id, listar_solicitacoes_disponiveis,
    cancelar_solicitacao, deletar_solicitacao
)
from ..services.auth_service_supabase import buscar_prestador_por_id

router = APIRouter(prefix="/solicitacoes")

# ============= ROTAS ESPECÍFICAS (antes das rotas com path params) =============

@router.get("/minhas", response_model=List[SolicitacaoResponse])
def listar_minhas_solicitacoes(
    cliente_id: int = Query(...),  # TODO: Extrair do token JWT
):
    """Cliente lista suas solicitações"""
    solicitacoes = listar_solicitacoes_cliente(cliente_id)
    
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
    prestador = buscar_prestador_por_id(prestador_id)
    if not prestador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prestador não encontrado"
        )
    
    print(f"Categorias do prestador: {prestador['categorias']}")
    solicitacoes = listar_solicitacoes_disponiveis(prestador['categorias'])
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
    solicitacao = criar_solicitacao(cliente_id, solicitacao_data)
    if not solicitacao:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar solicitação"
        )
    return solicitacao

@router.get("/{solicitacao_id}", response_model=SolicitacaoResponse)
def buscar_solicitacao(
    solicitacao_id: int,
):
    """Busca solicitação por ID"""
    solicitacao = buscar_solicitacao_por_id(solicitacao_id)
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
    sucesso = cancelar_solicitacao(solicitacao_id, cliente_id)
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
    sucesso = deletar_solicitacao(solicitacao_id, cliente_id)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Solicitação não encontrada"
        )
    return {"message": "Solicitação deletada com sucesso"}

