"""
Configuração global para testes pytest
"""
import pytest
import sys
import os
from pathlib import Path

# Adiciona o diretório do projeto ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

@pytest.fixture(autouse=True)
def setup_test_environment():
    """Configura ambiente de teste antes de cada teste"""
    # Configurações podem ser adicionadas aqui
    yield
    # Cleanup após cada teste

