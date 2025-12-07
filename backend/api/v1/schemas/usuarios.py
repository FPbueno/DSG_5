"""
Schemas Pydantic para Clientes e Prestadores (modo memória, sem validação rígida de email/endereço)
"""
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

# ============= SCHEMAS PARA CLIENTE =============

class ClienteBase(BaseModel):
    nome: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None

class ClienteCreate(ClienteBase):
    senha: str
    cpf: Optional[str] = None
    totp_secret: Optional[str] = None

class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None

class ClienteResponse(BaseModel):
    nome: str
    email: str
    telefone: str
    endereco: str
    id: int
    avaliacao_media: float
    created_at: str
    class Config:
        from_attributes = True

class ClienteLogin(BaseModel):
    email: Optional[str] = None
    senha: str
    codigo_2fa: str
    
class RegistrarClienteResponse(BaseModel):
    cliente: ClienteResponse
    codigo_2fa: str
    qr_code: str
    mensagem: str
# ============= SCHEMAS PARA PRESTADOR =============

class PrestadorBase(BaseModel):
    nome: str
    email: Optional[str] = None
    telefone: Optional[str] = None
    categorias: List[str]
    regioes_atendimento: List[str]

class PrestadorCreate(PrestadorBase):
    senha: str
    cpf_cnpj: Optional[str] = None
    portfolio: Optional[List[dict]] = None
    totp_secret: Optional[str] = None

class PrestadorUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    categorias: Optional[List[str]] = None
    regioes_atendimento: Optional[List[str]] = None
    portfolio: Optional[List[dict]] = None

class PrestadorResponse(PrestadorBase):
    id: int
    avaliacao_media: float
    portfolio: Optional[List[dict]] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PrestadorRegistroResponse(BaseModel):
    prestador: PrestadorResponse
    codigo_2fa: str
    qr_code: str
    mensagem: str


class PrestadorLogin(BaseModel):
    email: Optional[str] = None
    senha: str
    codigo_2fa: str

# ============= SCHEMA DE LOGIN GERAL =============

class LoginRequest(BaseModel):
    email: Optional[str] = None
    senha: str
    tipo_usuario: str  # "cliente" ou "prestador"

class LoginResponse(BaseModel):
    token: str
    tipo_usuario: str
    usuario_id: int
    nome: str
    email: str

class TwoFAVerifyRequest(BaseModel):
    email: Optional[str] = None
    tipo_usuario: str
    codigo: str  # 6 dígitos

class Login2FARequiredResponse(BaseModel):
    require_2fa: bool = True
    tipo_usuario: str
    usuario_id: int
    nome: str
    email: str
