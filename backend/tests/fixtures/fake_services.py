"""
Fakes e mocks de serviços para testes
"""
from typing import Dict, Any, Optional
from unittest.mock import Mock, MagicMock


class FakeSupabaseService:
    """Fake do Supabase para testes isolados"""
    
    def __init__(self):
        self._users = {}
        self._solicitacoes = {}
        self._orcamentos = {}
        self._avaliacoes = {}
        self._next_id = 1
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simula criação de usuário"""
        user_id = self._next_id
        self._next_id += 1
        user = {
            "id": user_id,
            **user_data
        }
        self._users[user_id] = user
        return user
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Simula busca de usuário por email"""
        for user in self._users.values():
            if user.get("email") == email:
                return user
        return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Simula busca de usuário por ID"""
        return self._users.get(user_id)
    
    def create_solicitacao(self, solicitacao_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simula criação de solicitação"""
        solicitacao_id = self._next_id
        self._next_id += 1
        solicitacao = {
            "id": solicitacao_id,
            "status": "pendente",
            **solicitacao_data
        }
        self._solicitacoes[solicitacao_id] = solicitacao
        return solicitacao
    
    def create_orcamento(self, orcamento_data: Dict[str, Any]) -> Dict[str, Any]:
        """Simula criação de orçamento"""
        orcamento_id = self._next_id
        self._next_id += 1
        orcamento = {
            "id": orcamento_id,
            "status": "pendente",
            **orcamento_data
        }
        self._orcamentos[orcamento_id] = orcamento
        return orcamento
    
    def clear(self):
        """Limpa todos os dados fake"""
        self._users.clear()
        self._solicitacoes.clear()
        self._orcamentos.clear()
        self._avaliacoes.clear()
        self._next_id = 1


class FakeMLService:
    """Fake do serviço de ML para testes"""
    
    def predict_price(self, description: str) -> float:
        """Retorna preço fixo para testes"""
        return 500.0
    
    def predict_category(self, description: str) -> str:
        """Retorna categoria fixa para testes"""
        return "Serviços Gerais"


def create_fake_ml_service() -> FakeMLService:
    """Factory para criar fake do ML service"""
    return FakeMLService()


def create_fake_supabase_service() -> FakeSupabaseService:
    """Factory para criar fake do Supabase"""
    return FakeSupabaseService()

