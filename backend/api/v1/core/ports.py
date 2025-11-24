"""
Ports (Interfaces) para Arquitetura Hexagonal
Define contratos que os adapters devem implementar
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional


class DatabasePort(ABC):
    """Port para operações de banco de dados"""
    
    @abstractmethod
    async def create_user(self, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cria um usuário"""
        pass
    
    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Busca usuário por email"""
        pass
    
    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Busca usuário por ID"""
        pass
    
    @abstractmethod
    async def create_solicitacao(self, solicitacao_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cria uma solicitação"""
        pass
    
    @abstractmethod
    async def get_solicitacao_by_id(self, solicitacao_id: int) -> Optional[Dict[str, Any]]:
        """Busca solicitação por ID"""
        pass
    
    @abstractmethod
    async def create_orcamento(self, orcamento_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cria um orçamento"""
        pass
    
    @abstractmethod
    async def get_orcamento_by_id(self, orcamento_id: int) -> Optional[Dict[str, Any]]:
        """Busca orçamento por ID"""
        pass
    
    @abstractmethod
    async def update_orcamento_status(self, orcamento_id: int, status: str) -> bool:
        """Atualiza status do orçamento"""
        pass


class MLPort(ABC):
    """Port para serviços de Machine Learning"""
    
    @abstractmethod
    def predict_price(self, description: str) -> float:
        """Prediz preço baseado na descrição"""
        pass
    
    @abstractmethod
    def predict_category(self, description: str) -> str:
        """Prediz categoria baseada na descrição"""
        pass
    
    @abstractmethod
    def calculate_price_limits(
        self,
        categoria: str,
        descricao: str,
        localizacao: str
    ) -> Dict[str, float]:
        """Calcula limites de preço (mínimo, sugerido, máximo)"""
        pass


class FileStoragePort(ABC):
    """Port para operações de armazenamento de arquivos"""
    
    @abstractmethod
    def read_file(self, file_path: str) -> bytes:
        """Lê arquivo do sistema"""
        pass
    
    @abstractmethod
    def file_exists(self, file_path: str) -> bool:
        """Verifica se arquivo existe"""
        pass

