"""
Serviço para integração com Supabase REST API
"""
import os
from supabase import create_client, Client
from typing import Optional, List, Dict, Any
from ..core.config import SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY

class SupabaseService:
    """Serviço para operações com Supabase"""
    
    def __init__(self):
        # Usa Service Role Key para operações administrativas
        service_key = SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY
        self.supabase: Client = create_client(SUPABASE_URL, service_key)
    
    # ============= CLIENTES =============
    
    def criar_cliente(self, cliente_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar novo cliente"""
        try:
            print(f"🔍 Dados do cliente: {cliente_data}")
            response = self.supabase.table('clientes').insert(cliente_data).execute()
            print(f"✅ Resposta do Supabase: {response.data}")
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"❌ Erro ao criar cliente: {e}")
            return None
    
    def buscar_cliente_por_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Buscar cliente por email"""
        try:
            response = self.supabase.table('clientes').select('*').eq('email', email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao buscar cliente: {e}")
            return None
    
    def buscar_cliente_por_id(self, cliente_id: int) -> Optional[Dict[str, Any]]:
        """Buscar cliente por ID"""
        try:
            response = self.supabase.table('clientes').select('*').eq('id', cliente_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao buscar cliente: {e}")
            return None
    
    # ============= PRESTADORES =============
    
    def criar_prestador(self, prestador_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar novo prestador"""
        try:
            response = self.supabase.table('prestadores').insert(prestador_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao criar prestador: {e}")
            return None
    
    def buscar_prestador_por_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Buscar prestador por email"""
        try:
            response = self.supabase.table('prestadores').select('*').eq('email', email).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao buscar prestador: {e}")
            return None
    
    def buscar_prestador_por_id(self, prestador_id: int) -> Optional[Dict[str, Any]]:
        """Buscar prestador por ID"""
        try:
            response = self.supabase.table('prestadores').select('*').eq('id', prestador_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao buscar prestador: {e}")
            return None
    
    # ============= SOLICITAÇÕES =============
    
    def criar_solicitacao(self, solicitacao_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar nova solicitação"""
        try:
            response = self.supabase.table('solicitacoes').insert(solicitacao_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao criar solicitação: {e}")
            return None
    
    def buscar_solicitacoes_por_cliente(self, cliente_id: int) -> List[Dict[str, Any]]:
        """Buscar solicitações por cliente"""
        try:
            response = self.supabase.table('solicitacoes').select('*').eq('cliente_id', cliente_id).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Erro ao buscar solicitações: {e}")
            return []
    
    # ============= ORÇAMENTOS =============
    
    def criar_orcamento(self, orcamento_data: Dict[str, Any]) -> Dict[str, Any]:
        """Criar novo orçamento"""
        try:
            response = self.supabase.table('orcamentos').insert(orcamento_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao criar orçamento: {e}")
            return None
    
    def buscar_orcamentos_por_solicitacao(self, solicitacao_id: int) -> List[Dict[str, Any]]:
        """Buscar orçamentos por solicitação"""
        try:
            response = self.supabase.table('orcamentos').select('*').eq('solicitacao_id', solicitacao_id).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Erro ao buscar orçamentos: {e}")
            return []
    
    # ============= MÉTODOS GENÉRICOS =============
    
    def get_client(self) -> Client:
        """Retorna o cliente Supabase"""
        return self.supabase
    
    def insert_data(self, table_name: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Inserir dados em qualquer tabela"""
        try:
            response = self.supabase.table(table_name).insert(data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao inserir dados em {table_name}: {e}")
            return None
    
    def fetch_all(self, table_name: str) -> List[Dict[str, Any]]:
        """Buscar todos os dados de uma tabela"""
        try:
            response = self.supabase.table(table_name).select('*').execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Erro ao buscar dados de {table_name}: {e}")
            return []
    
    def fetch_by_email(self, table_name: str, email: str) -> Optional[Dict[str, Any]]:
        """Buscar por email em qualquer tabela"""
        try:
            response = self.supabase.table(table_name).select('*').eq('email', email).limit(1).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Erro ao buscar por email em {table_name}: {e}")
            return None

# Instância global do serviço
supabase_service = SupabaseService()
