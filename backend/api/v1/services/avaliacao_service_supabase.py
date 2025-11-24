"""
Serviço de Avaliações usando Supabase REST
"""
from typing import Optional, Dict, Any
from ..services.supabase_service import supabase_service
from ..schemas import AvaliacaoCreate

# ============= AVALIAÇÕES =============

def criar_avaliacao(avaliacao_data: AvaliacaoCreate) -> Optional[Dict[str, Any]]:
    """Criar nova avaliação"""
    try:
        # Verificar se já existe avaliação para este orçamento
        existing = supabase_service.get_client().table("avaliacoes").select("id").eq("orcamento_id", avaliacao_data.orcamento_id).execute()
        
        if existing.data:
            print(f"Avaliação já existe para orçamento {avaliacao_data.orcamento_id}")
            return None
        
        data = {
            "orcamento_id": avaliacao_data.orcamento_id,
            "cliente_id": avaliacao_data.cliente_id,
            "prestador_id": avaliacao_data.prestador_id,
            "estrelas": avaliacao_data.estrelas,
            "comentario": avaliacao_data.comentario
        }
        
        # Criar avaliação
        resultado = supabase_service.insert_data("avaliacoes", data)
        
        if resultado:
            # Atualizar média do prestador
            atualizar_media_prestador(avaliacao_data.prestador_id)
        
        return resultado
    except Exception as e:
        print(f"Erro ao criar avaliação: {e}")
        return None

def obter_media_prestador(prestador_id: int) -> float:
    """Obter média de avaliações de um prestador"""
    try:
        response = supabase_service.get_client().table("avaliacoes").select("estrelas").eq("prestador_id", prestador_id).execute()
        
        if not response.data:
            return 0.0
        
        estrelas = [av['estrelas'] for av in response.data]
        return sum(estrelas) / len(estrelas) if estrelas else 0.0
    except Exception as e:
        print(f"Erro ao obter média do prestador: {e}")
        return 0.0

def contar_avaliacoes_prestador(prestador_id: int) -> int:
    """Contar total de avaliações de um prestador"""
    try:
        response = supabase_service.get_client().table("avaliacoes").select("id").eq("prestador_id", prestador_id).execute()
        return len(response.data) if response.data else 0
    except Exception as e:
        print(f"Erro ao contar avaliações: {e}")
        return 0

def atualizar_media_prestador(prestador_id: int) -> None:
    """Atualizar média de avaliações do prestador na tabela prestadores"""
    try:
        # Calcular nova média
        nova_media = obter_media_prestador(prestador_id)
        
        # Atualizar na tabela prestadores
        supabase_service.get_client().table("prestadores").update({
            "avaliacao_media": nova_media
        }).eq("id", prestador_id).execute()
        
        print(f"Média do prestador {prestador_id} atualizada para {nova_media}")
    except Exception as e:
        print(f"Erro ao atualizar média do prestador: {e}")
