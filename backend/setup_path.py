"""
Arquivo de inicialização que configura o PYTHONPATH
Este arquivo deve ser importado antes de qualquer outro módulo da aplicação
"""
import sys
from pathlib import Path

# Resolve o diretório backend (onde este arquivo está localizado)
backend_dir = Path(__file__).resolve().parent
backend_path = str(backend_dir)

# Adiciona ao sys.path se não estiver lá
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Exporta para uso em outros lugares se necessário
__all__ = ['backend_path']

