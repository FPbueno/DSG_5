"""
Serviço de Orçamentos usando Supabase REST
"""
from typing import Optional, List, Dict, Any
from ..services.supabase_service import supabase_service
from ..schemas import OrcamentoCreate
from datetime import datetime

# ============= ORÇAMENTOS =============

def criar_orcamento(prestador_id: int, solicitacao_id: int, orcamento_data: OrcamentoCreate, limites_ml: Dict[str, float] = None) -> Dict[str, Any]:
    """Criar novo orçamento"""
    try:
        # Se não foram fornecidos limites ML, usar valores padrão
        if not limites_ml:
            limites_ml = {
                "valor_minimo": 0.0,
                "valor_sugerido": 0.0,
                "valor_maximo": 0.0
            }
        
        data = {
            "prestador_id": prestador_id,
            "solicitacao_id": solicitacao_id,
            "valor_ml_minimo": limites_ml.get("valor_minimo", 0.0),
            "valor_ml_sugerido": limites_ml.get("valor_sugerido", 0.0),
            "valor_ml_maximo": limites_ml.get("valor_maximo", 0.0),
            "valor_proposto": orcamento_data.valor_proposto,
            "prazo_execucao": orcamento_data.prazo_execucao,
            "observacoes": orcamento_data.observacoes,
            "condicoes": orcamento_data.condicoes,
            "status": "aguardando"  # Valor padrão do enum
        }
        return supabase_service.insert_data("orcamentos", data)
    except Exception as e:
        print(f"Erro ao criar orçamento: {e}")
        return None

def listar_orcamentos_prestador(prestador_id: int) -> List[Dict[str, Any]]:
    """Listar orçamentos de um prestador"""
    try:
        response = supabase_service.get_client().table("orcamentos").select("*, solicitacoes(*), prestadores(*)").eq("prestador_id", prestador_id).order("created_at", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Erro ao listar orçamentos do prestador: {e}")
        return []

def buscar_orcamento_por_id(orcamento_id: int) -> Optional[Dict[str, Any]]:
    """Buscar orçamento por ID"""
    try:
        response = supabase_service.get_client().table("orcamentos").select("*, solicitacoes(*), prestadores(*)").eq("id", orcamento_id).limit(1).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Erro ao buscar orçamento: {e}")
        return None

def listar_orcamentos_solicitacao(solicitacao_id: int) -> List[Dict[str, Any]]:
    """Listar orçamentos de uma solicitação"""
    try:
        response = supabase_service.get_client().table("orcamentos").select("*, prestadores(*)").eq("solicitacao_id", solicitacao_id).order("created_at", desc=True).execute()
        return response.data if response.data else []
    except Exception as e:
        print(f"Erro ao listar orçamentos da solicitação: {e}")
        return []

def atualizar_status_orcamento(orcamento_id: int, novo_status: str) -> bool:
    """Atualizar status do orçamento"""
    try:
        response = supabase_service.get_client().table("orcamentos").update({"status": novo_status}).eq("id", orcamento_id).execute()
        return bool(response.data)
    except Exception as e:
        print(f"Erro ao atualizar status do orçamento: {e}")
        return False

def deletar_orcamento(orcamento_id: int, prestador_id: int) -> bool:
    """Deletar orçamento"""
    try:
        # Verifica se o orçamento pertence ao prestador
        orcamento = buscar_orcamento_por_id(orcamento_id)
        if not orcamento or orcamento['prestador_id'] != prestador_id:
            return False
        
        # Remove o orçamento
        response = supabase_service.get_client().table("orcamentos").delete().eq("id", orcamento_id).execute()
        return bool(response.data)
    except Exception as e:
        print(f"Erro ao deletar orçamento: {e}")
        return False

def aceitar_orcamento(orcamento_id: int, cliente_id: int) -> Optional[Dict[str, Any]]:
    """Cliente aceita um orçamento"""
    try:
        # Busca o orçamento
        orcamento = buscar_orcamento_por_id(orcamento_id)
        if not orcamento:
            return None
        
        # Verifica se o cliente tem permissão (via solicitação)
        from .solicitacao_service_supabase import buscar_solicitacao_por_id
        solicitacao = buscar_solicitacao_por_id(orcamento['solicitacao_id'])
        if not solicitacao or solicitacao['cliente_id'] != cliente_id:
            return None
        
        # Define início do serviço usando created_at da solicitação (ISO do Supabase).
        # Não usamos prazo_desejado porque vem em formato livre (ex: 22/11/2025).
        inicio_iso = None
        try:
            if solicitacao.get("created_at"):
                inicio_iso = solicitacao["created_at"]
        except Exception:
            inicio_iso = None

        update_data = {"status": "aceito"}
        if inicio_iso:
            # garante string em ISO; se já vier ISO do Supabase só reaproveita
            update_data["datetime_inicio"] = inicio_iso

        # Atualiza status para aceito + datetime_inicio (se definido)
        response = supabase_service.get_client().table("orcamentos").update(update_data).eq("id", orcamento_id).execute()
        
        if response.data:
            # Atualiza status da solicitação para "com_orcamentos"
            supabase_service.get_client().table("solicitacoes").update({
                "status": "com_orcamentos"
            }).eq("id", orcamento['solicitacao_id']).execute()
            
            return response.data[0]
        return None
    except Exception as e:
        print(f"Erro ao aceitar orçamento: {e}")
        return None

def marcar_realizado(orcamento_id: int, prestador_id: int) -> Optional[Dict[str, Any]]:
    """Prestador marca orçamento como realizado"""
    try:
        # Busca o orçamento
        orcamento = buscar_orcamento_por_id(orcamento_id)
        if not orcamento or orcamento['prestador_id'] != prestador_id:
            return None
        
        # Atualiza status para realizado e grava datetime_fim
        agora_iso = datetime.utcnow().isoformat()
        response = supabase_service.get_client().table("orcamentos").update({
            "status": "realizado",
            "datetime_fim": agora_iso
        }).eq("id", orcamento_id).execute()
        
        if response.data:
            # Atualiza status da solicitação para "fechada"
            supabase_service.get_client().table("solicitacoes").update({
                "status": "fechada"
            }).eq("id", orcamento['solicitacao_id']).execute()
            
            return response.data[0]
        return None
    except Exception as e:
        print(f"Erro ao marcar orçamento como realizado: {e}")
        return None
