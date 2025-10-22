"""
Serviço de Autenticação usando Supabase REST API
"""
from passlib.context import CryptContext
from ..schemas import ClienteCreate, PrestadorCreate
from typing import Optional, Union
from .supabase_service import supabase_service

# Contexto de criptografia de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_senha(senha: str) -> str:
    """Hash de senha usando bcrypt"""
    return pwd_context.hash(senha)

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Verifica se senha corresponde ao hash"""
    return pwd_context.verify(senha_plana, senha_hash)

# ============= CLIENTES =============

def criar_cliente(cliente_data: ClienteCreate) -> Optional[dict]:
    """Cria novo cliente usando Supabase"""
    try:
        cliente_dict = {
            "nome": cliente_data.nome,
            "email": cliente_data.email,
            "senha_hash": hash_senha(cliente_data.senha),
            "telefone": cliente_data.telefone,
            "cpf": cliente_data.cpf,
            "endereco": cliente_data.endereco,
            "avaliacao_media": 0.0
        }
        
        return supabase_service.criar_cliente(cliente_dict)
    except Exception as e:
        print(f"Erro ao criar cliente: {e}")
        return None

def buscar_cliente_por_email(email: str) -> Optional[dict]:
    """Busca cliente por email usando Supabase"""
    return supabase_service.buscar_cliente_por_email(email)

def buscar_cliente_por_id(cliente_id: int) -> Optional[dict]:
    """Busca cliente por ID usando Supabase"""
    return supabase_service.buscar_cliente_por_id(cliente_id)

def autenticar_cliente(email: str, senha: str) -> Optional[dict]:
    """Autentica cliente usando Supabase"""
    cliente = buscar_cliente_por_email(email)
    if cliente and verificar_senha(senha, cliente['senha_hash']):
        return cliente
    return None

# ============= PRESTADORES =============

def criar_prestador(prestador_data: PrestadorCreate) -> Optional[dict]:
    """Cria novo prestador usando Supabase"""
    try:
        prestador_dict = {
            "nome": prestador_data.nome,
            "email": prestador_data.email,
            "senha_hash": hash_senha(prestador_data.senha),
            "telefone": prestador_data.telefone,
            "cpf_cnpj": prestador_data.cpf_cnpj,
            "categorias": prestador_data.categorias,
            "regioes_atendimento": prestador_data.regioes_atendimento,
            "avaliacao_media": 0.0,
            "portfolio": prestador_data.portfolio
        }
        
        return supabase_service.criar_prestador(prestador_dict)
    except Exception as e:
        print(f"Erro ao criar prestador: {e}")
        return None

def buscar_prestador_por_email(email: str) -> Optional[dict]:
    """Busca prestador por email usando Supabase"""
    return supabase_service.buscar_prestador_por_email(email)

def buscar_prestador_por_id(prestador_id: int) -> Optional[dict]:
    """Busca prestador por ID usando Supabase"""
    return supabase_service.buscar_prestador_por_id(prestador_id)

def autenticar_prestador(email: str, senha: str) -> Optional[dict]:
    """Autentica prestador usando Supabase"""
    prestador = buscar_prestador_por_email(email)
    if prestador and verificar_senha(senha, prestador['senha_hash']):
        return prestador
    return None
