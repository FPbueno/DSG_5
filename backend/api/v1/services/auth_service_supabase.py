"""
Serviço de Autenticação usando Supabase REST API
"""
from passlib.context import CryptContext
from ..schemas import ClienteCreate, PrestadorCreate
from typing import Optional, Union
from .supabase_service import supabase_service

# Contexto de criptografia de senha
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


def hash_senha(senha: str) -> str:
    """Hash de senha usando bcrypt_sha256 (trunca para 72 bytes se necessário)"""
    # Bcrypt tem limite de 72 bytes
    if isinstance(senha, str):
        senha_bytes = senha.encode('utf-8')
        if len(senha_bytes) > 72:
            senha = senha_bytes[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(senha)

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Verifica se senha corresponde ao hash (trunca para 72 bytes se necessário)"""
    # Bcrypt tem limite de 72 bytes
    if isinstance(senha_plana, str):
        senha_bytes = senha_plana.encode('utf-8')
        if len(senha_bytes) > 72:
            senha_plana = senha_bytes[:72].decode('utf-8', errors='ignore')
    return pwd_context.verify(senha_plana, senha_hash)

# ============= CLIENTES =============

def criar_cliente(cliente_data: ClienteCreate, totp_secret: str = None, backup_codes: list = None) -> Optional[dict]:
    """Cria novo cliente no Supabase com suporte a 2FA e backup codes."""
    senha_hash = hash_senha(cliente_data.senha)

    data = {
        "nome": cliente_data.nome,
        "email": cliente_data.email,
        "telefone": cliente_data.telefone,
        "endereco": cliente_data.endereco,
        "senha_hash": senha_hash,  # ✅ coluna existente
        "totp_secret": totp_secret,
        "backup_codes": backup_codes or []
    }

    response = supabase_service.supabase.table("clientes").insert(data).execute()
    if response.data:
        return response.data[0]
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

def criar_prestador(prestador_data: PrestadorCreate, backup_codes: list = None) -> Optional[dict]:
    """Cria novo prestador usando Supabase com suporte a backup codes"""
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
            "portfolio": prestador_data.portfolio,
            "totp_secret": prestador_data.totp_secret,
            "backup_codes": backup_codes or []
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
