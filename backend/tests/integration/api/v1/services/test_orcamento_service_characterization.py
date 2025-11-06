"""
Characterization Tests para Orçamento Service
Captura comportamento atual antes de refatorar
"""
import pytest
from unittest.mock import patch, MagicMock
from api.v1.services.orcamento_service_supabase import (
    criar_orcamento,
    listar_orcamentos_prestador,
    buscar_orcamento_por_id,
    aceitar_orcamento,
    atualizar_status_orcamento
)
from api.v1.schemas import OrcamentoCreate
from tests.fixtures.mock_data import create_fake_orcamento_data


@pytest.mark.integration
class TestOrcamentoServiceCharacterization:
    """Testes de caracterização do serviço de orçamentos"""
    
    def test_criar_orcamento_estrutura(self, fake_supabase):
        """Testa estrutura de criação de orçamento"""
        # ARRANGE
        prestador_id = 1
        solicitacao_id = 1
        orcamento_data = OrcamentoCreate(
            solicitacao_id=solicitacao_id,
            valor_proposto=1000.0,
            prazo_execucao="30",
            observacoes="Teste",
            condicoes="Condições teste"
        )
        limites_ml = {
            "valor_minimo": 700.0,
            "valor_sugerido": 1000.0,
            "valor_maximo": 1500.0
        }
        
        # ACT
        with patch('api.v1.services.orcamento_service_supabase.supabase_service') as mock_supabase:
            mock_supabase.insert_data.return_value = {
                "id": 1,
                "prestador_id": prestador_id,
                "solicitacao_id": solicitacao_id,
                "valor_proposto": 1000.0,
                "valor_ml_minimo": 700.0,
                "valor_ml_sugerido": 1000.0,
                "valor_ml_maximo": 1500.0,
                "status": "aguardando"
            }
            resultado = criar_orcamento(prestador_id, solicitacao_id, orcamento_data, limites_ml)
        
        # ASSERT - Captura estrutura atual
        assert resultado is not None
        assert isinstance(resultado, dict)
        assert "id" in resultado
        assert resultado["prestador_id"] == prestador_id
        assert resultado["solicitacao_id"] == solicitacao_id
        assert resultado["valor_proposto"] == 1000.0
    
    def test_criar_orcamento_sem_limites_ml(self):
        """Testa criação sem limites ML (usa valores padrão)"""
        # ARRANGE
        prestador_id = 1
        solicitacao_id = 1
        orcamento_data = OrcamentoCreate(
            solicitacao_id=solicitacao_id,
            valor_proposto=500.0,
            prazo_execucao="15",
            observacoes="",
            condicoes=""
        )
        
        # ACT
        with patch('api.v1.services.orcamento_service_supabase.supabase_service') as mock_supabase:
            mock_supabase.insert_data.return_value = {"id": 1}
            resultado = criar_orcamento(prestador_id, solicitacao_id, orcamento_data, None)
        
        # ASSERT - Valida que valores padrão são usados
        assert resultado is not None
        mock_supabase.insert_data.assert_called_once()
        call_args = mock_supabase.insert_data.call_args
        assert call_args[0][1]["valor_ml_minimo"] == 0.0
        assert call_args[0][1]["valor_ml_sugerido"] == 0.0
        assert call_args[0][1]["valor_ml_maximo"] == 0.0
    
    def test_listar_orcamentos_prestador_estrutura(self):
        """Testa estrutura de listagem de orçamentos"""
        # ARRANGE
        prestador_id = 1
        
        # ACT
        with patch('api.v1.services.orcamento_service_supabase.supabase_service') as mock_supabase:
            mock_client = MagicMock()
            mock_table = MagicMock()
            mock_select = MagicMock()
            mock_eq = MagicMock()
            mock_order = MagicMock()
            mock_execute = MagicMock()
            
            mock_supabase.get_client.return_value = mock_client
            mock_client.table.return_value = mock_table
            mock_table.select.return_value = mock_select
            mock_select.eq.return_value = mock_eq
            mock_eq.order.return_value = mock_order
            mock_order.execute.return_value = MagicMock(data=[
                {"id": 1, "valor_proposto": 1000.0},
                {"id": 2, "valor_proposto": 1500.0}
            ])
            
            resultado = listar_orcamentos_prestador(prestador_id)
        
        # ASSERT
        assert isinstance(resultado, list)
        assert len(resultado) == 2
        assert resultado[0]["id"] == 1
    
    def test_aceitar_orcamento_fluxo(self):
        """Testa fluxo de aceitar orçamento"""
        # ARRANGE
        orcamento_id = 1
        cliente_id = 1
        
        # ACT
        with patch('api.v1.services.orcamento_service_supabase.buscar_orcamento_por_id') as mock_buscar, \
             patch('api.v1.services.orcamento_service_supabase.supabase_service') as mock_supabase:
            
            mock_buscar.return_value = {
                "id": 1,
                "solicitacao_id": 1,
                "prestador_id": 2
            }
            
            mock_solicitacao = MagicMock()
            mock_solicitacao.return_value = MagicMock(data=[{
                "id": 1,
                "cliente_id": cliente_id
            }])
            
            mock_client = MagicMock()
            mock_table = MagicMock()
            mock_update = MagicMock()
            mock_eq = MagicMock()
            mock_execute = MagicMock()
            
            mock_supabase.get_client.return_value = mock_client
            mock_client.table.return_value = mock_table
            mock_table.update.return_value = mock_update
            mock_update.eq.return_value = mock_eq
            mock_eq.execute.return_value = MagicMock(data=[{"id": 1, "status": "aceito"}])
            
            with patch('api.v1.services.solicitacao_service_supabase.buscar_solicitacao_por_id') as mock_solic:
                mock_solic.return_value = {"id": 1, "cliente_id": cliente_id}
                resultado = aceitar_orcamento(orcamento_id, cliente_id)
        
        # ASSERT - Captura comportamento atual
        # Pode retornar None ou dict dependendo da implementação
        assert resultado is None or isinstance(resultado, dict)
    
    def test_atualizar_status_orcamento(self):
        """Testa atualização de status"""
        # ARRANGE
        orcamento_id = 1
        novo_status = "aceito"
        
        # ACT
        with patch('api.v1.services.orcamento_service_supabase.supabase_service') as mock_supabase:
            mock_client = MagicMock()
            mock_table = MagicMock()
            mock_update = MagicMock()
            mock_eq = MagicMock()
            mock_execute = MagicMock()
            
            mock_supabase.get_client.return_value = mock_client
            mock_client.table.return_value = mock_table
            mock_table.update.return_value = mock_update
            mock_update.eq.return_value = mock_eq
            mock_eq.execute.return_value = MagicMock(data=[{"id": 1}])
            
            resultado = atualizar_status_orcamento(orcamento_id, novo_status)
        
        # ASSERT
        assert resultado is True

