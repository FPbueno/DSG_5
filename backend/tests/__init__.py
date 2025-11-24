"""
Arquivo de inicialização dos testes
Configura o PYTHONPATH antes de qualquer importação
"""
import sys
import os
from pathlib import Path

# Configuração do PYTHONPATH - DEVE ser feita ANTES de qualquer importação
backend_dir = Path(__file__).resolve().parent.parent
backend_path = str(backend_dir)

# Adiciona ao sys.path
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Configura variável de ambiente
current_pythonpath = os.environ.get('PYTHONPATH', '')
if backend_path not in current_pythonpath:
    new_pythonpath = backend_path + (os.pathsep if current_pythonpath else '') + current_pythonpath
    os.environ['PYTHONPATH'] = new_pythonpath

