import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv('.env')

# Configuração do banco de dados MySQL na nuvem
# URL obtida das variáveis de ambiente para segurança
DATABASE_URL = os.getenv("DATABASE_URL")

# Criar engine do SQLAlchemy com configurações SSL para MySQL na nuvem
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    echo=False,  # Mude para True para ver queries SQL no log
    connect_args={
        "ssl_disabled": False,
        "ssl_verify_cert": False,
        "ssl_verify_identity": False
    }
)

# Criar sessão local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para modelos
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
