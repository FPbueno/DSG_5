"""
Serviço de Autenticação para Clientes e Prestadores
"""
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from ..models.db_models import Cliente, Prestador
from ..schemas import ClienteCreate, PrestadorCreate
from typing import Optional, Union

# Contexto de criptografia de senha
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


def hash_senha(senha: str) -> str:
    """Hash de senha usando bcrypt_sha256 (trunca para 72 bytes se necessário)"""
    if isinstance(senha, str):
        senha_bytes = senha.encode('utf-8')
        if len(senha_bytes) > 72:
            senha = senha_bytes[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(senha)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Verifica se senha corresponde ao hash (trunca para 72 bytes se necessário)"""
    if isinstance(senha_plana, str):
        senha_bytes = senha_plana.encode('utf-8')
        if len(senha_bytes) > 72:
            senha_plana = senha_bytes[:72].decode('utf-8', errors='ignore')
    return pwd_context.verify(senha_plana, senha_hash)

# ============= CLIENTES =============

def criar_cliente(db: Session, cliente_data: ClienteCreate) -> Cliente:
    """Cria novo cliente no banco"""
    cliente = Cliente(
        nome=cliente_data.nome,
        email=cliente_data.email,
        senha_hash=hash_senha(cliente_data.senha),
        telefone=cliente_data.telefone,
        cpf=cliente_data.cpf,  # TODO: Implementar criptografia
        endereco=cliente_data.endereco
    )
    db.add(cliente)
    db.commit()
    db.refresh(cliente)
    return cliente

def autenticar_cliente(db: Session, email: str, senha: str) -> Optional[Cliente]:
    """Autentica cliente por email e senha"""
    cliente = db.query(Cliente).filter(Cliente.email == email).first()
    if not cliente:
        return None
    if not verificar_senha(senha, cliente.senha_hash):
        return None
    return cliente

def buscar_cliente_por_id(db: Session, cliente_id: int) -> Optional[Cliente]:
    """Busca cliente por ID"""
    return db.query(Cliente).filter(Cliente.id == cliente_id).first()

def buscar_cliente_por_email(db: Session, email: str) -> Optional[Cliente]:
    """Busca cliente por email"""
    return db.query(Cliente).filter(Cliente.email == email).first()

# ============= PRESTADORES =============

def criar_prestador(db: Session, prestador_data: PrestadorCreate) -> Prestador:
    """Cria novo prestador no banco"""
    prestador = Prestador(
        nome=prestador_data.nome,
        email=prestador_data.email,
        senha_hash=hash_senha(prestador_data.senha),
        telefone=prestador_data.telefone,
        cpf_cnpj=prestador_data.cpf_cnpj,  # TODO: Implementar criptografia
        categorias=prestador_data.categorias,
        regioes_atendimento=prestador_data.regioes_atendimento,
        portfolio=prestador_data.portfolio
    )
    db.add(prestador)
    db.commit()
    db.refresh(prestador)
    return prestador

def autenticar_prestador(db: Session, email: str, senha: str) -> Optional[Prestador]:
    """Autentica prestador por email e senha"""
    prestador = db.query(Prestador).filter(Prestador.email == email).first()
    if not prestador:
        return None
    if not verificar_senha(senha, prestador.senha_hash):
        return None
    return prestador

def buscar_prestador_por_id(db: Session, prestador_id: int) -> Optional[Prestador]:
    """Busca prestador por ID"""
    return db.query(Prestador).filter(Prestador.id == prestador_id).first()

def buscar_prestador_por_email(db: Session, email: str) -> Optional[Prestador]:
    """Busca prestador por email"""
    return db.query(Prestador).filter(Prestador.email == email).first()

