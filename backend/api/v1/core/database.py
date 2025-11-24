import sys
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Garante que o diretório backend está no sys.path ANTES de tentar importar
backend_dir = Path(__file__).resolve().parent.parent.parent.parent
backend_path = str(backend_dir)
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Importa config - tenta múltiplas estratégias para garantir compatibilidade
DATABASE_URL = None

try:
    from .config import DATABASE_URL
except (ImportError, ModuleNotFoundError):
    try:
        from api.v1.core.config import DATABASE_URL
    except (ImportError, ModuleNotFoundError):
        # Fallback: import direto do arquivo usando importlib
        try:
            import importlib.util
            # Tenta múltiplos caminhos possíveis (começa pelo mais confiável)
            current_file = Path(__file__).resolve()
            possible_paths = [
                current_file.parent / "config.py",  # Relativo ao arquivo atual (mais confiável)
                backend_dir / "api" / "v1" / "core" / "config.py",
            ]
            config_path = None
            for path in possible_paths:
                if path.exists():
                    config_path = path
                    break
            
            if config_path and config_path.exists():
                try:
                    spec = importlib.util.spec_from_file_location("api.v1.core.config", config_path)
                    if spec and spec.loader:
                        config_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(config_module)
                        DATABASE_URL = getattr(config_module, "DATABASE_URL", None)
                except Exception:
                    pass  # Se falhar, usa variável de ambiente abaixo
        except Exception:
            pass  # Se falhar, usa variável de ambiente abaixo

# Se ainda não tiver valor, usa variável de ambiente
if not DATABASE_URL:
    DATABASE_URL = os.getenv("DATABASE_URL")

# Configuração do banco de dados
DEFAULT_SQLITE_URL = "sqlite:///./app_test.db"

def _create_engine():
    if DATABASE_URL:
        return create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=300,
            echo=False,
            connect_args={"sslmode": "require"},
        )
    # Fallback para testes/CI sem banco configurado
    return create_engine(
        DEFAULT_SQLITE_URL,
        connect_args={"check_same_thread": False},
        echo=False,
    )

engine = _create_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency para obter sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    """Criar todas as tabelas no banco de dados"""
    Base.metadata.create_all(bind=engine)
