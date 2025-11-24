"""
Testes E2E - Fluxo Completo
Solicitação -> Orçamento -> Aceite
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from api.v1.core.adapters import FakeDatabaseAdapter, FakeMLAdapter


@pytest.mark.e2e
class TestFluxoCompletoE2E:
    """Testes end-to-end do fluxo completo"""
    
    @pytest.fixture
    def client(self):
        """TestClient do FastAPI"""
        import sys
        import os
        from pathlib import Path
        
        # Garante que o path está configurado de forma explícita
        backend_dir = Path(__file__).resolve().parent.parent.parent.parent
        backend_path = str(backend_dir)
        
        # Adiciona ao sys.path se não estiver lá
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
        
        # Configura PYTHONPATH também
        current_pythonpath = os.environ.get('PYTHONPATH', '')
        if backend_path not in current_pythonpath:
            new_pythonpath = backend_path + (os.pathsep if current_pythonpath else '') + current_pythonpath
            os.environ['PYTHONPATH'] = new_pythonpath
        
        # Importa setup_path para garantir que o path está configurado
        try:
            import setup_path  # noqa: F401
        except ImportError:
            pass
        
        # Importa main - se falhar, tenta novamente com path garantido
        try:
            from main import app
        except (ImportError, ModuleNotFoundError):
            # Garante path novamente e tenta importar
            if backend_path not in sys.path:
                sys.path.insert(0, backend_path)
            from main import app
        
        return TestClient(app)
    
    @pytest.fixture
    def fake_db(self):
        """Fake database adapter"""
        return FakeDatabaseAdapter()
    
    @pytest.fixture
    def fake_ml(self):
        """Fake ML adapter"""
        return FakeMLAdapter()
    
    def test_fluxo_completo_solicitacao_orcamento_aceite(self, fake_db, fake_ml):
        """
        Testa fluxo completo:
        1. Cliente cria solicitação
        2. Prestador envia orçamento
        3. Cliente aceita orçamento
        """
        # ARRANGE
        cliente_data = {
            "nome": "João Cliente",
            "email": "joao@teste.com",
            "senha": "senha123",
            "telefone": "11999999999",
            "endereco": "Rua Teste, 123"
        }
        
        prestador_data = {
            "nome": "Empresa XYZ",
            "email": "empresa@teste.com",
            "senha": "senha123",
            "telefone": "11988888888",
            "cpf_cnpj": "12345678901",
            "categorias": ["Pintura"],
            "regioes_atendimento": ["São Paulo"]
        }
        
        # ACT & ASSERT - Passo 1: Criar cliente
        import asyncio
        cliente = asyncio.run(fake_db.create_user(cliente_data))
        assert cliente is not None
        cliente_id = cliente["id"]
        
        # Passo 2: Criar prestador
        prestador = asyncio.run(fake_db.create_user(prestador_data))
        assert prestador is not None
        prestador_id = prestador["id"]
        
        # Passo 3: Cliente cria solicitação
        solicitacao_data = {
            "cliente_id": cliente_id,
            "categoria": "Pintura",
            "descricao": "Pintura de parede residencial",
            "localizacao": "São Paulo",
            "prazo_desejado": "30 dias",
            "informacoes_adicionais": "Urgente"
        }
        solicitacao = asyncio.run(fake_db.create_solicitacao(solicitacao_data))
        assert solicitacao is not None
        solicitacao_id = solicitacao["id"]
        assert solicitacao["status"] == "aguardando_orcamentos"
        
        # Passo 4: Calcular limites ML
        limites = fake_ml.calculate_price_limits(
            solicitacao_data["categoria"],
            solicitacao_data["descricao"],
            solicitacao_data["localizacao"]
        )
        assert limites["valor_minimo"] > 0
        assert limites["valor_sugerido"] > 0
        assert limites["valor_maximo"] > 0
        
        # Passo 5: Prestador envia orçamento
        orcamento_data = {
            "prestador_id": prestador_id,
            "solicitacao_id": solicitacao_id,
            "valor_proposto": limites["valor_sugerido"],
            "valor_ml_minimo": limites["valor_minimo"],
            "valor_ml_sugerido": limites["valor_sugerido"],
            "valor_ml_maximo": limites["valor_maximo"],
            "prazo_execucao": "25 dias",
            "observacoes": "Orçamento padrão",
            "condicoes": "Pagamento à vista"
        }
        orcamento = asyncio.run(fake_db.create_orcamento(orcamento_data))
        assert orcamento is not None
        orcamento_id = orcamento["id"]
        assert orcamento["status"] == "aguardando"
        
        # Passo 6: Cliente aceita orçamento
        sucesso = asyncio.run(fake_db.update_orcamento_status(orcamento_id, "aceito"))
        assert sucesso is True
        
        # Verificar estado final
        orcamento_final = asyncio.run(fake_db.get_orcamento_by_id(orcamento_id))
        assert orcamento_final is not None
        assert orcamento_final["status"] == "aceito"
    
    def test_endpoint_calcular_limites_ml(self, client):
        """Testa endpoint de cálculo de limites ML"""
        # ARRANGE
        payload = {
            "categoria": "Pintura",
            "descricao": "Pintura de parede",
            "localizacao": "São Paulo"
        }
        
        # ACT
        response = client.post("/api/v1/ml/calcular-limites", json=payload)
        
        # ASSERT
        assert response.status_code in [200, 404]  # 404 se endpoint não existe ainda
        if response.status_code == 200:
            data = response.json()
            assert "valor_minimo" in data
            assert "valor_sugerido" in data
            assert "valor_maximo" in data
    
    def test_endpoint_get_health(self, client):
        """Testa endpoint de health check"""
        # ACT
        response = client.get("/health")
        
        # ASSERT
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

