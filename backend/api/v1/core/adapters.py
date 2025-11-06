"""
Adapters - Implementações concretas dos Ports
Real Adapters: Implementações reais (Supabase, ML real)
Fake Adapters: Implementações para testes
"""
import pickle
import os
from typing import Dict, Any, Optional
from .ports import DatabasePort, MLPort, FileStoragePort


# ============= REAL ADAPTERS =============

class SupabaseAdapter(DatabasePort):
    """Adapter real para Supabase"""
    
    def __init__(self, supabase_service):
        self.supabase_service = supabase_service
    
    async def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cria usuário no Supabase"""
        return self.supabase_service.criar_cliente(user_data)
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Busca usuário por email no Supabase"""
        return self.supabase_service.buscar_cliente_por_email(email)
    
    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Busca usuário por ID no Supabase"""
        return self.supabase_service.buscar_cliente_por_id(user_id)
    
    async def create_solicitacao(self, solicitacao_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cria solicitação no Supabase"""
        return self.supabase_service.insert_data("solicitacoes", solicitacao_data)
    
    async def get_solicitacao_by_id(self, solicitacao_id: int) -> Optional[Dict[str, Any]]:
        """Busca solicitação por ID no Supabase"""
        response = self.supabase_service.get_client().table("solicitacoes").select("*").eq("id", solicitacao_id).limit(1).execute()
        return response.data[0] if response.data else None
    
    async def create_orcamento(self, orcamento_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cria orçamento no Supabase"""
        return self.supabase_service.insert_data("orcamentos", orcamento_data)
    
    async def get_orcamento_by_id(self, orcamento_id: int) -> Optional[Dict[str, Any]]:
        """Busca orçamento por ID no Supabase"""
        response = self.supabase_service.get_client().table("orcamentos").select("*").eq("id", orcamento_id).limit(1).execute()
        return response.data[0] if response.data else None
    
    async def update_orcamento_status(self, orcamento_id: int, status: str) -> bool:
        """Atualiza status do orçamento no Supabase"""
        response = self.supabase_service.get_client().table("orcamentos").update({"status": status}).eq("id", orcamento_id).execute()
        return bool(response.data)


class SklearnMLAdapter(MLPort):
    """Adapter real para modelos ML scikit-learn"""
    
    def __init__(self):
        self._load_models()
    
    def _load_models(self):
        """Carrega modelos ML"""
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        MODELS_DIR = os.path.join(BASE_DIR, "models")
        
        try:
            with open(os.path.join(MODELS_DIR, "price_model.pkl"), "rb") as f:
                self.price_model = pickle.load(f)
            with open(os.path.join(MODELS_DIR, "price_vectorizer.pkl"), "rb") as f:
                self.price_vectorizer = pickle.load(f)
            with open(os.path.join(MODELS_DIR, "category_model.pkl"), "rb") as f:
                self.category_model = pickle.load(f)
            with open(os.path.join(MODELS_DIR, "category_vectorizer.pkl"), "rb") as f:
                self.category_vectorizer = pickle.load(f)
            self.models_loaded = True
        except Exception as e:
            print(f"⚠️ Aviso: Modelos ML não carregados: {e}")
            self.models_loaded = False
    
    def predict_price(self, description: str) -> float:
        """Prediz preço usando modelo real"""
        if not self.models_loaded:
            return 500.0
        
        try:
            X = self.price_vectorizer.transform([description])
            preco = self.price_model.predict(X)[0]
            return float(preco)
        except Exception as e:
            print(f"Erro ao predizer preço: {e}")
            return 500.0
    
    def predict_category(self, description: str) -> str:
        """Prediz categoria usando modelo real"""
        if not self.models_loaded:
            return "Serviços Gerais"
        
        try:
            X = self.category_vectorizer.transform([description])
            categoria = self.category_model.predict(X)[0]
            return str(categoria)
        except Exception as e:
            print(f"Erro ao predizer categoria: {e}")
            return "Serviços Gerais"
    
    def calculate_price_limits(
        self,
        categoria: str,
        descricao: str,
        localizacao: str
    ) -> Dict[str, float]:
        """Calcula limites de preço"""
        texto_completo = f"{categoria} {descricao} {localizacao}"
        valor_sugerido = self.predict_price(texto_completo)
        
        valor_minimo = valor_sugerido * 0.7
        valor_maximo = valor_sugerido * 1.5
        
        return {
            "valor_minimo": round(valor_minimo, 2),
            "valor_sugerido": round(valor_sugerido, 2),
            "valor_maximo": round(valor_maximo, 2),
            "categoria_predita": self.predict_category(descricao)
        }


class FileSystemAdapter(FileStoragePort):
    """Adapter real para sistema de arquivos"""
    
    def read_file(self, file_path: str) -> bytes:
        """Lê arquivo do sistema"""
        with open(file_path, "rb") as f:
            return f.read()
    
    def file_exists(self, file_path: str) -> bool:
        """Verifica se arquivo existe"""
        return os.path.exists(file_path)


# ============= FAKE ADAPTERS (para testes) =============

class FakeDatabaseAdapter(DatabasePort):
    """Adapter fake para testes - em memória"""
    
    def __init__(self):
        self._users = {}
        self._solicitacoes = {}
        self._orcamentos = {}
        self._next_id = 1
    
    async def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cria usuário fake"""
        user_id = self._next_id
        self._next_id += 1
        user = {"id": user_id, **user_data}
        self._users[user_id] = user
        return user
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Busca usuário fake por email"""
        for user in self._users.values():
            if user.get("email") == email:
                return user
        return None
    
    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Busca usuário fake por ID"""
        return self._users.get(user_id)
    
    async def create_solicitacao(self, solicitacao_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cria solicitação fake"""
        solicitacao_id = self._next_id
        self._next_id += 1
        solicitacao = {"id": solicitacao_id, "status": "aguardando_orcamentos", **solicitacao_data}
        self._solicitacoes[solicitacao_id] = solicitacao
        return solicitacao
    
    async def get_solicitacao_by_id(self, solicitacao_id: int) -> Optional[Dict[str, Any]]:
        """Busca solicitação fake por ID"""
        return self._solicitacoes.get(solicitacao_id)
    
    async def create_orcamento(self, orcamento_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cria orçamento fake"""
        orcamento_id = self._next_id
        self._next_id += 1
        orcamento = {"id": orcamento_id, "status": "aguardando", **orcamento_data}
        self._orcamentos[orcamento_id] = orcamento
        return orcamento
    
    async def get_orcamento_by_id(self, orcamento_id: int) -> Optional[Dict[str, Any]]:
        """Busca orçamento fake por ID"""
        return self._orcamentos.get(orcamento_id)
    
    async def update_orcamento_status(self, orcamento_id: int, status: str) -> bool:
        """Atualiza status do orçamento fake"""
        if orcamento_id in self._orcamentos:
            self._orcamentos[orcamento_id]["status"] = status
            return True
        return False
    
    def clear(self):
        """Limpa todos os dados fake"""
        self._users.clear()
        self._solicitacoes.clear()
        self._orcamentos.clear()
        self._next_id = 1


class FakeMLAdapter(MLPort):
    """Adapter fake para ML - retorna valores fixos"""
    
    def predict_price(self, description: str) -> float:
        """Retorna preço fixo para testes"""
        return 500.0
    
    def predict_category(self, description: str) -> str:
        """Retorna categoria fixa para testes"""
        return "Serviços Gerais"
    
    def calculate_price_limits(
        self,
        categoria: str,
        descricao: str,
        localizacao: str
    ) -> Dict[str, float]:
        """Calcula limites fake"""
        valor_sugerido = 500.0
        return {
            "valor_minimo": 350.0,
            "valor_sugerido": valor_sugerido,
            "valor_maximo": 750.0,
            "categoria_predita": "Serviços Gerais"
        }


class FakeFileStorageAdapter(FileStoragePort):
    """Adapter fake para arquivos - em memória"""
    
    def __init__(self):
        self._files = {}
    
    def read_file(self, file_path: str) -> bytes:
        """Lê arquivo fake"""
        return self._files.get(file_path, b"")
    
    def file_exists(self, file_path: str) -> bool:
        """Verifica se arquivo fake existe"""
        return file_path in self._files
    
    def add_file(self, file_path: str, content: bytes):
        """Adiciona arquivo fake (método helper para testes)"""
        self._files[file_path] = content

