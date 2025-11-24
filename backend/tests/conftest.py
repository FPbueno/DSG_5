"""
Configuração global para testes pytest
"""
# IMPORTANTE: Configurações de path DEVEM vir antes de qualquer importação de módulos da aplicação
import sys
import os
from pathlib import Path

# Configuração do PYTHONPATH - DEVE ser feita ANTES de qualquer importação de módulos da aplicação
# Resolve o diretório backend (pai do diretório tests)
backend_dir = Path(__file__).resolve().parent.parent
backend_path = str(backend_dir)

# Adiciona o diretório backend ao sys.path se não estiver lá
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Configura variável de ambiente PYTHONPATH
current_pythonpath = os.environ.get('PYTHONPATH', '')
if backend_path not in current_pythonpath:
    new_pythonpath = backend_path + (os.pathsep if current_pythonpath else '') + current_pythonpath
    os.environ['PYTHONPATH'] = new_pythonpath

# Configura variáveis de ambiente mockadas para evitar erros durante importação
# Isso permite que módulos que dependem do Supabase sejam importados sem erro
os.environ.setdefault("SUPABASE_URL", "https://mock.supabase.co")
os.environ.setdefault("SUPABASE_ANON_KEY", "mock-anon-key")
os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "mock-service-key")
os.environ.setdefault("CI", "true")  # Marca como ambiente de CI

# Agora pode importar pytest e outros módulos
import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Configura ambiente de teste antes de cada teste"""
    # Configurações podem ser adicionadas aqui
    yield
    # Cleanup após cada teste


@pytest.fixture
def fake_supabase():
    """Fixture que fornece fake do Supabase para testes isolados"""
    from tests.fixtures.fake_services import FakeSupabaseService
    service = FakeSupabaseService()
    yield service
    service.clear()  # Limpa após teste


@pytest.fixture
def fake_ml_service():
    """Fixture que fornece fake do serviço de ML para testes"""
    from tests.fixtures.fake_services import FakeMLService
    return FakeMLService()


@pytest.fixture
def fake_database_adapter():
    """Fixture que fornece FakeDatabaseAdapter (Ports & Adapters)"""
    from api.v1.core.adapters import FakeDatabaseAdapter
    adapter = FakeDatabaseAdapter()
    yield adapter
    adapter.clear()


@pytest.fixture
def fake_ml_adapter():
    """Fixture que fornece FakeMLAdapter (Ports & Adapters)"""
    from api.v1.core.adapters import FakeMLAdapter
    return FakeMLAdapter()


@pytest.fixture
def mock_data():
    """Fixture que fornece factories de dados fake"""
    from tests.fixtures.mock_data import (
        create_fake_user_data,
        create_fake_client_data,
        create_fake_solicitacao_data,
        create_fake_orcamento_data,
        create_fake_service_data,
    )
    return {
        "user": create_fake_user_data,
        "client": create_fake_client_data,
        "solicitacao": create_fake_solicitacao_data,
        "orcamento": create_fake_orcamento_data,
        "service": create_fake_service_data,
    }


@pytest.fixture
def test_client():
    """Fixture que fornece TestClient do FastAPI"""
    from fastapi.testclient import TestClient
    from main import app
    return TestClient(app)


# Configuração de markers padrão
def pytest_configure(config):
    """Registra markers customizados"""
    config.addinivalue_line("markers", "unit: Testes unitários")
    config.addinivalue_line("markers", "integration: Testes de integração")
    config.addinivalue_line("markers", "e2e: Testes end-to-end")
    config.addinivalue_line("markers", "slow: Testes lentos")
    config.addinivalue_line("markers", "requires_db: Testes que requerem banco")
    config.addinivalue_line("markers", "requires_network: Testes que requerem rede")

