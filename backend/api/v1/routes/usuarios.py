"""
Rotas de Autenticação e Gestão de Usuários (modo memória, sem DB/Supabase)
2FA desabilitado: login conclui direto com token.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Dict, Any, Optional

from ..schemas import (
    ClienteCreate,
    ClienteResponse,
    PrestadorCreate,
    PrestadorResponse,
    LoginRequest,
    LoginResponse,
    RegistrarClienteResponse,
    PrestadorRegistroResponse,
)
from ..core.security import get_rsa_public_key_pem
from ..schemas.usuarios import TwoFAVerifyRequest
import itertools

router = APIRouter()

# Armazenamento em memória
_clientes: Dict[int, Dict[str, Any]] = {}
_prestadores: Dict[int, Dict[str, Any]] = {}
_seq_cliente = itertools.count(1)
_seq_prestador = itertools.count(1)


# Helpers de memória
def _salvar_cliente(data: ClienteCreate) -> dict:
    cid = next(_seq_cliente)
    cliente = {
        "id": cid,
        "nome": data.nome,
        "email": data.email or "",
        "telefone": data.telefone or "",
        "endereco": data.endereco or "",
        "senha": data.senha,
        "totp_secret": None,
        "created_at": "now",
        "avaliacao_media": 0.0,
    }
    _clientes[cid] = cliente
    return cliente


def _salvar_prestador(data: PrestadorCreate) -> dict:
    pid = next(_seq_prestador)
    prestador = {
        "id": pid,
        "nome": data.nome,
        "email": data.email or "",
        "telefone": data.telefone or "",
        "categorias": data.categorias,
        "regioes_atendimento": data.regioes_atendimento,
        "portfolio": data.portfolio or [],
        "senha": data.senha,
        "totp_secret": None,
        "created_at": "now",
        "avaliacao_media": 0.0,
    }
    _prestadores[pid] = prestador
    return prestador


def _buscar_cliente_por_email(email: str) -> Optional[dict]:
    if not email:
        return None
    return next((c for c in _clientes.values() if c.get("email") == email), None)


def _buscar_prestador_por_email(email: str) -> Optional[dict]:
    if not email:
        return None
    return next((p for p in _prestadores.values() if p.get("email") == email), None)


def _buscar_cliente_por_id(cid: int) -> Optional[dict]:
    return _clientes.get(cid)


def _buscar_prestador_por_id(pid: int) -> Optional[dict]:
    return _prestadores.get(pid)


def _autenticar_usuario(tipo: str, email: str, senha: str) -> Optional[dict]:
    pool = _clientes if tipo == "cliente" else _prestadores
    for u in pool.values():
        if (email is None or u.get("email") == email) and u.get("senha") == senha:
            return u
    return None


# ============= TESTE =============
@router.post("/teste")
def teste_endpoint(dados: dict):
    """Endpoint de teste para debugar"""
    print(f"Dados brutos recebidos: {dados}")
    return {"message": "Dados recebidos com sucesso", "dados": dados}


# ============= REGISTRO =============
@router.post("/registrar", response_model=RegistrarClienteResponse)
def registrar_cliente(cliente_data: ClienteCreate):
    """Registra novo cliente sem 2FA (memória)"""
    if cliente_data.email and _buscar_cliente_por_email(cliente_data.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Desabilita 2FA e aceita a senha como enviada
    cliente = _salvar_cliente(cliente_data)

    return {
        "cliente": ClienteResponse(
            id=cliente["id"],
            nome=cliente["nome"],
            email=cliente["email"],
            telefone=cliente["telefone"],
            endereco=cliente["endereco"],
            avaliacao_media=cliente.get("avaliacao_media", 0.0) or 0.0,
            created_at=cliente["created_at"],
        ),
        "codigo_2fa": "",
        "qr_code": "",
        "mensagem": "Cadastro realizado sem 2FA.",
    }


@router.post(
    "/prestadores/registrar",
    response_model=PrestadorRegistroResponse,
    status_code=status.HTTP_201_CREATED,
)
def registrar_prestador(prestador_data: PrestadorCreate):
    if prestador_data.email and _buscar_prestador_por_email(prestador_data.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    prestador = _salvar_prestador(prestador_data)

    return {
        "prestador": PrestadorResponse(
            id=prestador["id"],
            nome=prestador["nome"],
            email=prestador["email"],
            telefone=prestador["telefone"],
            categorias=prestador["categorias"],
            regioes_atendimento=prestador["regioes_atendimento"],
            avaliacao_media=prestador.get("avaliacao_media", 0.0) or 0.0,
            portfolio=prestador.get("portfolio") or [],
            created_at=prestador["created_at"],
        ),
        "codigo_2fa": "",
        "qr_code": "",
        "mensagem": "Cadastro realizado sem 2FA.",
    }


# ============= LOGIN =============
@router.get("/public-key")
def get_public_key():
    """Retorna a chave pública RSA para criptografia no frontend"""
    return {"public_key": get_rsa_public_key_pem()}


@router.post("/login")
def login(login_data: LoginRequest):
    """
    Autenticação de email e senha. 2FA desabilitado, retorna token direto.
    """
    senha_decrypt = login_data.senha

    if login_data.tipo_usuario == "cliente":
        usuario = _autenticar_usuario("cliente", login_data.email, senha_decrypt)
    elif login_data.tipo_usuario == "prestador":
        usuario = _autenticar_usuario("prestador", login_data.email, senha_decrypt)
    else:
        raise HTTPException(status_code=400, detail="Tipo de usuário inválido")

    if not usuario:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    token = f"token_{login_data.tipo_usuario}_{usuario['id']}"
    return LoginResponse(
        token=token,
        tipo_usuario=login_data.tipo_usuario,
        usuario_id=usuario["id"],
        nome=usuario["nome"],
        email=usuario.get("email", ""),
    )


@router.post("/login-2fa", response_model=LoginResponse)
def login_2fa(data: TwoFAVerifyRequest):
    """
    2FA desabilitado: aceita qualquer código e retorna token se usuário existir.
    """
    if data.tipo_usuario == "cliente":
        usuario = _buscar_cliente_por_email(data.email or "")
    elif data.tipo_usuario == "prestador":
        usuario = _buscar_prestador_por_email(data.email or "")
    else:
        raise HTTPException(status_code=400, detail="Tipo de usuário inválido")

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    token = f"token_{data.tipo_usuario}_{usuario['id']}"
    return LoginResponse(
        token=token,
        tipo_usuario=data.tipo_usuario,
        usuario_id=usuario["id"],
        nome=usuario["nome"],
        email=usuario["email"],
    )


# ============= GESTÃO DE PRESTADORES =============
@router.get("/prestadores/{prestador_id}", response_model=PrestadorResponse)
def buscar_prestador(prestador_id: int):
    """Busca dados do prestador"""
    prestador = _buscar_prestador_por_id(prestador_id)
    if not prestador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prestador não encontrado",
        )

    return PrestadorResponse(
        id=prestador["id"],
        nome=prestador["nome"],
        email=prestador["email"],
        telefone=prestador.get("telefone"),
        categorias=prestador.get("categorias") or [],
        regioes_atendimento=prestador.get("regioes_atendimento") or [],
        avaliacao_media=prestador.get("avaliacao_media", 0.0) or 0.0,
        portfolio=prestador.get("portfolio") or [],
        created_at=prestador["created_at"],
    )


class AtualizarCategoriasRequest(BaseModel):
    categorias: list[str]


@router.put("/prestadores/{prestador_id}")
def atualizar_prestador(
    prestador_id: int,
    dados: AtualizarCategoriasRequest,
):
    """Atualiza categorias do prestador"""
    prestador = _buscar_prestador_por_id(prestador_id)
    if not prestador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prestador não encontrado",
        )

    prestador["categorias"] = dados.categorias

    return {"success": True, "message": "Categorias atualizadas com sucesso"}
