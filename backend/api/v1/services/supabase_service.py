"""
Serviço para integração com Supabase REST API
"""
import sys
import os
from pathlib import Path
from supabase import create_client, Client
from typing import Optional, List, Dict, Any

# Garante que o diretório backend está no sys.path ANTES de tentar importar
backend_dir = Path(__file__).resolve().parent.parent.parent.parent
backend_path = str(backend_dir)
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Importa config - tenta múltiplas estratégias para garantir compatibilidade
SUPABASE_URL = None
SUPABASE_ANON_KEY = None
SUPABASE_SERVICE_ROLE_KEY = None

try:
    from api.v1.core.config import SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY
except (ImportError, ModuleNotFoundError):
    # Fallback: import direto do arquivo usando importlib
    try:
        import importlib.util
        # Tenta múltiplos caminhos possíveis (começa pelo mais confiável)
        current_file = Path(__file__).resolve()
        possible_paths = [
            current_file.parent.parent / "core" / "config.py",  # Relativo ao arquivo atual (mais confiável)
            backend_dir / "api" / "v1" / "core" / "config.py",
        ]
        config_path = None
        for path in possible_paths:
            if path.exists():
                config_path = path
                break
        
        if config_path and config_path.exists():
            try:
                spec = importlib.util.spec_from_file_location("api.v1.core.config", config_path)
                if spec and spec.loader:
                    config_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(config_module)
                    SUPABASE_URL = getattr(config_module, "SUPABASE_URL", None)
                    SUPABASE_ANON_KEY = getattr(config_module, "SUPABASE_ANON_KEY", None)
                    SUPABASE_SERVICE_ROLE_KEY = getattr(config_module, "SUPABASE_SERVICE_ROLE_KEY", None)
            except Exception:
                pass  # Se falhar, usa variáveis de ambiente abaixo
    except Exception:
        pass  # Se falhar, usa variáveis de ambiente abaixo

# Se ainda não tiver valores, usa variáveis de ambiente
if not SUPABASE_URL:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
if not SUPABASE_ANON_KEY:
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
if not SUPABASE_SERVICE_ROLE_KEY:
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

class SupabaseService:
    """Serviço para operações com Supabase"""
    
    def __init__(self, supabase_url: Optional[str] = None, supabase_key: Optional[str] = None):
        # Usa Service Role Key para operações administrativas
        url = supabase_url or SUPABASE_URL
        service_key = supabase_key or SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY
        
        if not url:
            raise ValueError("supabase_url is required. Set SUPABASE_URL environment variable.")
        if not service_key:
            raise ValueError("supabase_key is required. Set SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY environment variable.")
        
        self.supabase: Client = create_client(url, service_key)
    
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

# Instância global do serviço (lazy initialization)
_supabase_service_instance: Optional['SupabaseService'] = None

def get_supabase_service() -> 'SupabaseService':
    """Retorna instância do serviço Supabase (singleton lazy)"""
    global _supabase_service_instance
    if _supabase_service_instance is None:
        try:
            _supabase_service_instance = SupabaseService()
        except Exception as e:
            # Em ambiente de teste/CI, tenta criar com valores mockados
            import os
            if os.getenv("CI") or os.getenv("PYTEST_CURRENT_TEST"):
                # Usa valores mockados se disponíveis
                mock_url = os.getenv("SUPABASE_URL", "https://mock.supabase.co")
                mock_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY", "mock-key")
                try:
                    _supabase_service_instance = SupabaseService(supabase_url=mock_url, supabase_key=mock_key)
                except Exception:
                    # Se ainda falhar, levanta exceção com mensagem clara
                    raise RuntimeError(
                        "SupabaseService não pode ser inicializado. "
                        "Configure variáveis de ambiente ou use mocks nos testes."
                    ) from e
            else:
                raise
    return _supabase_service_instance

# Para compatibilidade com código existente, criamos um proxy que se comporta como instância
class _SupabaseServiceProxy:
    """Proxy que cria a instância real apenas quando necessário"""
    def __getattr__(self, name):
        return getattr(get_supabase_service(), name)

supabase_service = _SupabaseServiceProxy()
