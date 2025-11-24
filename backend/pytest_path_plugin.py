"""
Plugin do pytest para configurar o PYTHONPATH antes de qualquer importação
Este arquivo DEVE ser executado antes de qualquer outro módulo ser importado
"""
import sys
import os
from pathlib import Path

# Resolve o diretório backend
backend_dir = Path(__file__).resolve().parent
backend_path = str(backend_dir)

# Adiciona ao sys.path ANTES de qualquer importação
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Configura variável de ambiente
current_pythonpath = os.environ.get('PYTHONPATH', '')
if backend_path not in current_pythonpath:
    new_pythonpath = backend_path + (os.pathsep if current_pythonpath else '') + current_pythonpath
    os.environ['PYTHONPATH'] = new_pythonpath

def pytest_configure(config):
    """Hook executado quando o pytest é configurado"""
    # Garante que o path está configurado
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)

