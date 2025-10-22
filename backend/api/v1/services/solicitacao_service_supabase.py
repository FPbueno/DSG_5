"""
Serviço de Solicitações usando Supabase REST
"""
from typing import Optional, List, Dict, Any
from ..services.supabase_service import supabase_service
from ..schemas import SolicitacaoCreate

# ============= SOLICITAÇÕES =============

def criar_solicitacao(cliente_id: int, solicitacao_data: SolicitacaoCreate) -> Dict[str, Any]:
    """Criar nova solicitação"""
    try:
        data = {
            "cliente_id": cliente_id,
            "categoria": solicitacao_data.categoria,
            "descricao": solicitacao_data.descricao,
            "localizacao": solicitacao_data.localizacao,
            "prazo_desejado": solicitacao_data.prazo_desejado,
            "informacoes_adicionais": solicitacao_data.informacoes_adicionais,
            "status": "aguardando_orcamentos"  # Valor válido do enum
        }
        return supabase_service.insert_data("solicitacoes", data)
    except Exception as e:
        print(f"Erro ao criar solicitação: {e}")
        return None

def listar_solicitacoes_cliente(cliente_id: int) -> List[Dict[str, Any]]:
    """Listar solicitações de um cliente"""
    try:
        response = supabase_service.get_client().table("solicitacoes").select("*").eq("cliente_id", cliente_id).order("created_at", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Erro ao listar solicitações do cliente: {e}")
        return []

def buscar_solicitacao_por_id(solicitacao_id: int) -> Optional[Dict[str, Any]]:
    """Buscar solicitação por ID"""
    try:
        response = supabase_service.get_client().table("solicitacoes").select("*").eq("id", solicitacao_id).limit(1).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Erro ao buscar solicitação: {e}")
        return None

def listar_solicitacoes_disponiveis(categorias: List[str]) -> List[Dict[str, Any]]:
    """Listar solicitações disponíveis para prestadores"""
    try:
        # Busca solicitações abertas que correspondem às categorias do prestador
        response = supabase_service.get_client().table("solicitacoes").select("*, clientes(nome, avaliacao_media)").eq("status", "aguardando_orcamentos").in_("categoria", categorias).order("created_at", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Erro ao listar solicitações disponíveis: {e}")
        return []

def cancelar_solicitacao(solicitacao_id: int, cliente_id: int) -> bool:
    """Cancelar solicitação"""
    try:
        # Verifica se a solicitação pertence ao cliente
        solicitacao = buscar_solicitacao_por_id(solicitacao_id)
        if not solicitacao or solicitacao['cliente_id'] != cliente_id:
            return False
        
        # Atualiza status para cancelada
        response = supabase_service.get_client().table("solicitacoes").update({"status": "cancelada"}).eq("id", solicitacao_id).execute()
        return bool(response.data)
    except Exception as e:
        print(f"Erro ao cancelar solicitação: {e}")
        return False

def deletar_solicitacao(solicitacao_id: int, cliente_id: int) -> bool:
    """Deletar solicitação"""
    try:
        # Verifica se a solicitação pertence ao cliente
        solicitacao = buscar_solicitacao_por_id(solicitacao_id)
        if not solicitacao or solicitacao['cliente_id'] != cliente_id:
            return False
        
        # Remove a solicitação
        response = supabase_service.get_client().table("solicitacoes").delete().eq("id", solicitacao_id).execute()
        return bool(response.data)
    except Exception as e:
        print(f"Erro ao deletar solicitação: {e}")
        return False
