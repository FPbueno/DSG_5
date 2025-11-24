import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Garante que o diretório backend está no sys.path antes de importar config
backend_dir = Path(__file__).resolve().parent.parent.parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from .config import DATABASE_URL

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
