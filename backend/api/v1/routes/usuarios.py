"""
Rotas de Autenticação e Gestão de Usuários (Clientes e Prestadores)
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from ..schemas import (
    ClienteCreate, ClienteResponse,
    PrestadorCreate, PrestadorResponse,
    LoginRequest, LoginResponse
)
from ..services.auth_service_supabase import (
    criar_cliente, criar_prestador,
    autenticar_cliente, autenticar_prestador,
    buscar_cliente_por_email, buscar_prestador_por_email,
    buscar_prestador_por_id
)

router = APIRouter()

# ============= TESTE =============

@router.post("/teste")
def teste_endpoint(dados: dict):
    """Endpoint de teste para debugar"""
    print(f"🔍 Dados brutos recebidos: {dados}")
    return {"message": "Dados recebidos com sucesso", "dados": dados}

# ============= REGISTRO =============

@router.post("/clientes/registrar", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def registrar_cliente(cliente_data: ClienteCreate):
    """Registra novo cliente"""
    print(f"🔍 Dados recebidos: {cliente_data}")
    print(f"🔍 Tipo dos dados: {type(cliente_data)}")
    print(f"🔍 Email: {cliente_data.email}")
    print(f"🔍 Nome: {cliente_data.nome}")
    
    # Verifica se email já existe
    if buscar_cliente_por_email(cliente_data.email):
        print("❌ Email já cadastrado")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    print("✅ Email disponível, criando cliente...")
    cliente = criar_cliente(cliente_data)
    if not cliente:
        print("❌ Falha ao criar cliente")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar cliente"
        )
    
    print(f"✅ Cliente criado com sucesso: {cliente}")
    return ClienteResponse(
        id=cliente['id'],
        nome=cliente['nome'],
        email=cliente['email'],
        telefone=cliente['telefone'],
        endereco=cliente['endereco'],
        avaliacao_media=cliente['avaliacao_media'],
        created_at=cliente.get('created_at')
    )

@router.post("/prestadores/registrar", response_model=PrestadorResponse, status_code=status.HTTP_201_CREATED)
def registrar_prestador(prestador_data: PrestadorCreate):
    """Registra novo prestador"""
    # Verifica se email já existe
    if buscar_prestador_por_email(prestador_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    prestador = criar_prestador(prestador_data)
    if not prestador:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar prestador"
        )
    
    return PrestadorResponse(
        id=prestador['id'],
        nome=prestador['nome'],
        email=prestador['email'],
        telefone=prestador['telefone'],
        categorias=prestador['categorias'],
        regioes_atendimento=prestador['regioes_atendimento'],
        avaliacao_media=prestador['avaliacao_media'],
        portfolio=prestador['portfolio'],
        created_at=prestador.get('created_at')
    )

# ============= LOGIN =============

@router.post("/login", response_model=LoginResponse)
def login(login_data: LoginRequest):
    """
    Login unificado para clientes e prestadores
    """
    if login_data.tipo_usuario == "cliente":
        usuario = autenticar_cliente(login_data.email, login_data.senha)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        
        return LoginResponse(
            token=f"token_cliente_{usuario['id']}",  # TODO: Implementar JWT real
            tipo_usuario="cliente",
            usuario_id=usuario['id'],
            nome=usuario['nome'],
            email=usuario['email']
        )
    
    elif login_data.tipo_usuario == "prestador":
        usuario = autenticar_prestador(login_data.email, login_data.senha)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos"
            )
        
        return LoginResponse(
            token=f"token_prestador_{usuario['id']}",  # TODO: Implementar JWT real
            tipo_usuario="prestador",
            usuario_id=usuario['id'],
            nome=usuario['nome'],
            email=usuario['email']
        )
    
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de usuário inválido. Use 'cliente' ou 'prestador'"
        )

# ============= GESTÃO DE PRESTADORES =============

@router.get("/prestadores/{prestador_id}", response_model=PrestadorResponse)
def buscar_prestador(prestador_id: int):
    """Busca dados do prestador"""
    prestador = buscar_prestador_por_id(prestador_id)
    if not prestador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prestador não encontrado"
        )
    
    return PrestadorResponse(
        id=prestador['id'],
        nome=prestador['nome'],
        email=prestador['email'],
        telefone=prestador['telefone'],
        categorias=prestador['categorias'],
        regioes_atendimento=prestador['regioes_atendimento'],
        avaliacao_media=prestador['avaliacao_media'],
        portfolio=prestador['portfolio'],
        created_at=prestador.get('created_at')
    )

class AtualizarCategoriasRequest(BaseModel):
    categorias: list[str]

@router.put("/prestadores/{prestador_id}")
def atualizar_prestador(
    prestador_id: int,
    dados: AtualizarCategoriasRequest
):
    """Atualiza categorias do prestador"""
    prestador = buscar_prestador_por_id(prestador_id)
    if not prestador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prestador não encontrado"
        )
    
    # Atualiza categorias no Supabase
    try:
        from ..services.supabase_service import supabase_service
        response = supabase_service.get_client().table("prestadores").update({
            "categorias": dados.categorias
        }).eq("id", prestador_id).execute()
        
        if response.data:
            return {"success": True, "message": "Categorias atualizadas com sucesso"}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar categorias"
            )
    except Exception as e:
        print(f"Erro ao atualizar prestador: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

