"""
Rotas de Orçamentos
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from ..schemas import (
    OrcamentoCreate, OrcamentoResponse,
    OrcamentoComLimites, CalcularLimitesRequest, CalcularLimitesResponse
)
from ..services.orcamento_service_supabase import (
    criar_orcamento, listar_orcamentos_solicitacao,
    listar_orcamentos_prestador, buscar_orcamento_por_id,
    atualizar_status_orcamento, deletar_orcamento, aceitar_orcamento,
    marcar_realizado
)
from ..services.solicitacao_service_supabase import buscar_solicitacao_por_id
from ..services.ml_service import calcular_limites_preco

router = APIRouter(prefix="/orcamentos")

# ============= PRESTADOR =============

@router.get("/calcular-limites/{solicitacao_id}", response_model=CalcularLimitesResponse)
def calcular_limites_endpoint(
    solicitacao_id: int,
):
    """
    Calcula limites de preço (mínimo, sugerido, máximo) para uma solicitação
    Apenas para prestador usar como referência
    """
    solicitacao = buscar_solicitacao_por_id(solicitacao_id)
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
    solicitacao = buscar_solicitacao_por_id(orcamento_data.solicitacao_id)
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
    orcamento = criar_orcamento(prestador_id, orcamento_data.solicitacao_id, orcamento_data, limites)
    
    if not orcamento:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar orçamento"
        )
    
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
    orc = marcar_realizado(orcamento_id, prestador_id)
    if not orc.get('id'):
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
    orcamentos = listar_orcamentos_prestador(prestador_id)
    
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
    sucesso = deletar_orcamento(orcamento_id, prestador_id)
    
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
    solicitacao = buscar_solicitacao_por_id(solicitacao_id)
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
    
    orcamentos = listar_orcamentos_solicitacao(solicitacao_id)
    
    # Formata resposta (SEM os limites do ML)
    resultado = []
    for orc in orcamentos:
        # Verificar se já foi avaliado
        ja_avaliado = False
        try:
            from ..services.supabase_service import supabase_service
            avaliacao_response = supabase_service.get_client().table("avaliacoes").select("id").eq("orcamento_id", orc['id']).execute()
            ja_avaliado = len(avaliacao_response.data) > 0
        except Exception as e:
            print(f"Erro ao verificar avaliação: {e}")
            ja_avaliado = False
        
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
            "ja_avaliado": ja_avaliado
        })
    
    return resultado

@router.put("/{orcamento_id}/aceitar", response_model=OrcamentoResponse)
def aceitar_orcamento_endpoint(
    orcamento_id: int,
    cliente_id: int = Query(...),  # TODO: Extrair do token JWT
):
    """Cliente aceita um orçamento"""
    orcamento = aceitar_orcamento(orcamento_id, cliente_id)
    
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
    try:
        # Busca orçamentos realizados do cliente via Supabase
        from ..services.supabase_service import supabase_service
        
        response = supabase_service.get_client().table("orcamentos").select(
            "*, solicitacoes!inner(*), prestadores(*)"
        ).eq("status", "realizado").eq("solicitacoes.cliente_id", cliente_id).execute()
        
        orcamentos = response.data if response.data else []
        
        resultado = []
        for orc in orcamentos:
            # Verificar se já foi avaliado
            ja_avaliado = False
            try:
                from ..services.supabase_service import supabase_service
                avaliacao_response = supabase_service.get_client().table("avaliacoes").select("id").eq("orcamento_id", orc['id']).execute()
                ja_avaliado = len(avaliacao_response.data) > 0
            except Exception as e:
                print(f"Erro ao verificar avaliação: {e}")
                ja_avaliado = False
            
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
                "prestador_nome": orc.get('prestadores', {}).get('nome', 'N/A'),
                "prestador_avaliacao": orc.get('prestadores', {}).get('avaliacao_media', 0.0),
                "ja_avaliado": ja_avaliado
            })
        
        return resultado
    except Exception as e:
        print(f"Erro ao listar orçamentos realizados: {e}")
        return []

