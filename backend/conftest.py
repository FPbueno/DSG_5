"""
Conftest na raiz do backend para configurar o path ANTES de qualquer importação
Este arquivo é carregado pelo pytest antes de qualquer outro conftest ou teste
"""
import sys
from pathlib import Path

# Configura o path ANTES de qualquer importação
backend_dir = Path(__file__).resolve().parent
backend_path = str(backend_dir)

# Adiciona o diretório backend ao sys.path
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Importa setup_path para garantir dupla proteção
try:
    import setup_path  # noqa: F401
except ImportError:
    pass

