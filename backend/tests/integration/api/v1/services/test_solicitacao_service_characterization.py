"""
Characterization Tests para Solicitação Service
"""
import pytest
from unittest.mock import patch, MagicMock
from api.v1.services.solicitacao_service_supabase import (
    criar_solicitacao,
    listar_solicitacoes_cliente,
    buscar_solicitacao_por_id,
    listar_solicitacoes_disponiveis,
    cancelar_solicitacao
)
from api.v1.schemas import SolicitacaoCreate


@pytest.mark.integration
class TestSolicitacaoServiceCharacterization:
    """Testes de caracterização do serviço de solicitações"""
    
    def test_criar_solicitacao_estrutura(self):
        """Testa estrutura de criação de solicitação"""
        # ARRANGE
        cliente_id = 1
        solicitacao_data = SolicitacaoCreate(
            categoria="Pintura",
            descricao="Pintura de parede",
            localizacao="São Paulo",
            prazo_desejado="30",
            informacoes_adicionais="Urgente"
        )
        
        # ACT
        with patch('api.v1.services.solicitacao_service_supabase.supabase_service') as mock_supabase:
            mock_supabase.insert_data.return_value = {
                "id": 1,
                "cliente_id": cliente_id,
                "categoria": "Pintura",
                "status": "aguardando_orcamentos"
            }
            resultado = criar_solicitacao(cliente_id, solicitacao_data)
        
        # ASSERT
        assert resultado is not None
        assert isinstance(resultado, dict)
        assert resultado["cliente_id"] == cliente_id
        assert resultado["categoria"] == "Pintura"
        assert resultado["status"] == "aguardando_orcamentos"
    
    def test_listar_solicitacoes_cliente(self):
        """Testa listagem de solicitações do cliente"""
        # ARRANGE
        cliente_id = 1
        
        # ACT
        with patch('api.v1.services.solicitacao_service_supabase.supabase_service') as mock_supabase:
            mock_client = MagicMock()
            mock_table = MagicMock()
            mock_select = MagicMock()
            mock_eq = MagicMock()
            mock_order = MagicMock()
            
            mock_supabase.get_client.return_value = mock_client
            mock_client.table.return_value = mock_table
            mock_table.select.return_value = mock_select
            mock_select.eq.return_value = mock_eq
            mock_eq.order.return_value = mock_order
            mock_order.execute.return_value = MagicMock(data=[
                {"id": 1, "cliente_id": cliente_id},
                {"id": 2, "cliente_id": cliente_id}
            ])
            
            resultado = listar_solicitacoes_cliente(cliente_id)
        
        # ASSERT
        assert isinstance(resultado, list)
        assert len(resultado) == 2
    
    def test_buscar_solicitacao_por_id(self):
        """Testa busca de solicitação por ID"""
        # ARRANGE
        solicitacao_id = 1
        
        # ACT
        with patch('api.v1.services.solicitacao_service_supabase.supabase_service') as mock_supabase:
            mock_client = MagicMock()
            mock_table = MagicMock()
            mock_select = MagicMock()
            mock_eq = MagicMock()
            mock_limit = MagicMock()
            
            mock_supabase.get_client.return_value = mock_client
            mock_client.table.return_value = mock_table
            mock_table.select.return_value = mock_select
            mock_select.eq.return_value = mock_eq
            mock_eq.limit.return_value = mock_limit
            mock_limit.execute.return_value = MagicMock(data=[{"id": 1}])
            
            resultado = buscar_solicitacao_por_id(solicitacao_id)
        
        # ASSERT
        assert resultado is not None
        assert resultado["id"] == 1
    
    def test_listar_solicitacoes_disponiveis_com_categorias(self):
        """Testa listagem de solicitações disponíveis filtradas por categorias"""
        # ARRANGE
        categorias = ["Pintura", "Limpeza"]
        
        # ACT
        with patch('api.v1.services.solicitacao_service_supabase.supabase_service') as mock_supabase:
            mock_client = MagicMock()
            mock_table = MagicMock()
            mock_select = MagicMock()
            mock_eq = MagicMock()
            mock_in = MagicMock()
            mock_order = MagicMock()
            
            mock_supabase.get_client.return_value = mock_client
            mock_client.table.return_value = mock_table
            mock_table.select.return_value = mock_select
            mock_select.eq.return_value = mock_eq
            mock_eq.in_.return_value = mock_in
            mock_in.order.return_value = mock_order
            mock_order.execute.return_value = MagicMock(data=[
                {"id": 1, "categoria": "Pintura"},
                {"id": 2, "categoria": "Limpeza"}
            ])
            
            resultado = listar_solicitacoes_disponiveis(categorias)
        
        # ASSERT
        assert isinstance(resultado, list)
    
    def test_cancelar_solicitacao_com_permissao(self):
        """Testa cancelamento de solicitação com permissão"""
        # ARRANGE
        solicitacao_id = 1
        cliente_id = 1
        
        # ACT
        with patch('api.v1.services.solicitacao_service_supabase.buscar_solicitacao_por_id') as mock_buscar, \
             patch('api.v1.services.solicitacao_service_supabase.supabase_service') as mock_supabase:
            
            mock_buscar.return_value = {
                "id": solicitacao_id,
                "cliente_id": cliente_id
            }
            
            mock_client = MagicMock()
            mock_table = MagicMock()
            mock_update = MagicMock()
            mock_eq = MagicMock()
            
            mock_supabase.get_client.return_value = mock_client
            mock_client.table.return_value = mock_table
            mock_table.update.return_value = mock_update
            mock_update.eq.return_value = mock_eq
            mock_eq.execute.return_value = MagicMock(data=[{"id": 1}])
            
            resultado = cancelar_solicitacao(solicitacao_id, cliente_id)
        
        # ASSERT
        assert resultado is True

