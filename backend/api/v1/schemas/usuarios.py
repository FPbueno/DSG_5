"""
Schemas Pydantic para Clientes e Prestadores
"""
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime

# ============= SCHEMAS PARA CLIENTE =============

class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None
    endereco: Optional[str] = None

class ClienteCreate(ClienteBase):
    senha: str
    cpf: Optional[str] = None

class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    endereco: Optional[str] = None

class ClienteResponse(ClienteBase):
    id: int
    avaliacao_media: float
    created_at: datetime

    class Config:
        from_attributes = True

class ClienteLogin(BaseModel):
    email: EmailStr
    senha: str

# ============= SCHEMAS PARA PRESTADOR =============

class PrestadorBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None
    categorias: List[str]
    regioes_atendimento: List[str]

class PrestadorCreate(PrestadorBase):
    senha: str
    cpf_cnpj: Optional[str] = None
    portfolio: Optional[List[dict]] = None

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
    created_at: datetime

    class Config:
        from_attributes = True

class PrestadorLogin(BaseModel):
    email: EmailStr
    senha: str

# ============= SCHEMA DE LOGIN GERAL =============

class LoginRequest(BaseModel):
    email: EmailStr
    senha: str
    tipo_usuario: str  # "cliente" ou "prestador"

class LoginResponse(BaseModel):
    token: str
    tipo_usuario: str
    usuario_id: int
    nome: str
    email: str

