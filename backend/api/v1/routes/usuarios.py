"""
Rotas de Autenticação e Gestão de Usuários (Clientes e Prestadores)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..core.database import get_db
from ..schemas import (
    ClienteCreate, ClienteResponse,
    PrestadorCreate, PrestadorResponse,
    LoginRequest, LoginResponse
)
from ..services.auth_service import (
    criar_cliente, criar_prestador,
    autenticar_cliente, autenticar_prestador,
    buscar_cliente_por_email, buscar_prestador_por_email,
    buscar_prestador_por_id
)

router = APIRouter()

# ============= REGISTRO =============

@router.post("/clientes/registrar", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def registrar_cliente(cliente_data: ClienteCreate, db: Session = Depends(get_db)):
    """Registra novo cliente"""
    # Verifica se email já existe
    if buscar_cliente_por_email(db, cliente_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    cliente = criar_cliente(db, cliente_data)
    return cliente

@router.post("/prestadores/registrar", response_model=PrestadorResponse, status_code=status.HTTP_201_CREATED)
def registrar_prestador(prestador_data: PrestadorCreate, db: Session = Depends(get_db)):
    """Registra novo prestador"""
    # Verifica se email já existe
    if buscar_prestador_por_email(db, prestador_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    prestador = criar_prestador(db, prestador_data)
    return prestador

# ============= LOGIN =============

@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login unificado para clientes e prestadores
    """
    if login_data.tipo_usuario == "cliente":
        usuario = autenticar_cliente(db, login_data.email, login_data.senha)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        
        return LoginResponse(
            token=f"token_cliente_{usuario.id}",  # TODO: Implementar JWT real
            tipo_usuario="cliente",
            usuario_id=usuario.id,
            nome=usuario.nome,
            email=usuario.email
        )
    
    elif login_data.tipo_usuario == "prestador":
        usuario = autenticar_prestador(db, login_data.email, login_data.senha)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        
        return LoginResponse(
            token=f"token_prestador_{usuario.id}",  # TODO: Implementar JWT real
            tipo_usuario="prestador",
            usuario_id=usuario.id,
            nome=usuario.nome,
            email=usuario.email
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de usuário inválido. Use 'cliente' ou 'prestador'"
        )

# ============= GESTÃO DE PRESTADORES =============

@router.get("/prestadores/{prestador_id}", response_model=PrestadorResponse)
def buscar_prestador(prestador_id: int, db: Session = Depends(get_db)):
    """Busca dados do prestador"""
    prestador = buscar_prestador_por_id(db, prestador_id)
    if not prestador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prestador não encontrado"
        )
    return prestador

class AtualizarCategoriasRequest(BaseModel):
    categorias: list[str]

@router.put("/prestadores/{prestador_id}")
def atualizar_prestador(
    prestador_id: int,
    dados: AtualizarCategoriasRequest,
    db: Session = Depends(get_db)
):
    """Atualiza categorias do prestador"""
    prestador = buscar_prestador_por_id(db, prestador_id)
    if not prestador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prestador não encontrado"
        )
    
    prestador.categorias = dados.categorias
    
    db.commit()
    db.refresh(prestador)
    return {"success": True}

