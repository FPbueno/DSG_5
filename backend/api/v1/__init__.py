# API v1 Package
import sys
from pathlib import Path

# Garante que o diretório backend está no sys.path
backend_dir = Path(__file__).resolve().parent.parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))
