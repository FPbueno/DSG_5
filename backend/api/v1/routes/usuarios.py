"""
Rotas de Autenticação e Gestão de Usuários (Clientes e Prestadores)
"""
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from ..schemas import (
    ClienteCreate, ClienteResponse,
    PrestadorCreate, PrestadorResponse,
    LoginRequest, LoginResponse, RegistrarClienteResponse, PrestadorRegistroResponse
)
from ..services.auth_service import ( 
    criar_cliente, criar_prestador,
    autenticar_cliente, autenticar_prestador,
    buscar_cliente_por_email, buscar_prestador_por_email,
    buscar_prestador_por_id
)
from ..core.security import get_rsa_public_key_pem, decrypt_rsa_password
from api.v1.schemas.usuarios import TwoFAVerifyRequest
import pyotp
from api.v1.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# ============= 2FA UTILS =============

def gerar_2fa_secret(email: str, tipo_usuario: str):
    """Gera segredo TOTP (apenas o código secreto base32, sem QR Code)"""
    totp_secret = pyotp.random_base32()
    print(f"🔐 Segredo 2FA gerado: {totp_secret}")
    return totp_secret

# ============= TESTE =============

@router.post("/teste")
def teste_endpoint(dados: dict):
    """Endpoint de teste para debugar"""
    print(f"🔍 Dados brutos recebidos: {dados}")
    return {"message": "Dados recebidos com sucesso", "dados": dados}

# ============= REGISTRO =============

@router.post("/registrar", response_model=RegistrarClienteResponse)
def registrar_cliente(cliente_data: ClienteCreate, db: Session = Depends(get_db)):
    """Registra novo cliente com 2FA (usando SQLAlchemy para consistência)"""
    if buscar_cliente_por_email(db, cliente_data.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Gerar segredo 2FA
    totp_secret = gerar_2fa_secret(cliente_data.email, "cliente")

    # Descriptografa a senha recebida (vem criptografada do front-end)
    senha_plain = decrypt_rsa_password(cliente_data.senha)
    
    # Substitua a senha no cliente_data com a plain (o criar_cliente fará o hash)
    cliente_data.senha = senha_plain

    # Criar cliente via SQLAlchemy (passando db e totp_secret)
    cliente = criar_cliente(db, cliente_data)
    if not cliente:
        raise HTTPException(status_code=500, detail="Erro ao criar cliente")

    # Adicione totp_secret ao cliente (assumindo que o modelo Cliente tem um campo para isso)
    cliente.totp_secret = totp_secret  # Ajuste se o modelo não tiver
    db.commit()

    return {
        "cliente": ClienteResponse(
            id=cliente.id,
            nome=cliente.nome,
            email=cliente.email,
            telefone=cliente.telefone,
            endereco=cliente.endereco,
            avaliacao_media=cliente.avaliacao_media or 0.0, 
            created_at=cliente.created_at
        ),
        "codigo_2fa": totp_secret,
        "mensagem": "Use este código secreto no app autenticador (Google Authenticator, Authy etc.) para ativar o 2FA. Insira manualmente o código base32."
    }

@router.post(
    "/prestadores/registrar",
    response_model=PrestadorRegistroResponse,
    status_code=status.HTTP_201_CREATED
)
def registrar_prestador(prestador_data: PrestadorCreate, db: Session = Depends(get_db)):
    if buscar_prestador_por_email(db, prestador_data.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    secret = gerar_2fa_secret(prestador_data.email, "prestador")
    
    # Mesmo processo: descriptografar
    senha_plain = decrypt_rsa_password(prestador_data.senha)
    prestador_data.senha = senha_plain
    prestador_data.totp_secret = secret

    prestador = criar_prestador(db, prestador_data)
    if not prestador:
        raise HTTPException(status_code=500, detail="Erro ao criar prestador")

    return {
        "prestador": PrestadorResponse(
            id=prestador.id,
            nome=prestador.nome,
            email=prestador.email,
            telefone=prestador.telefone,
            categorias=prestador.categorias,
            regioes_atendimento=prestador.regioes_atendimento,
            avaliacao_media=prestador.avaliacao_media,
            portfolio=prestador.portfolio,
            created_at=prestador.created_at
        ),
        "codigo_2fa": secret,
        "mensagem": "Use este código no Google Authenticator ou Authy para ativar o 2FA."
    }

# ============= LOGIN =============

@router.get("/public-key")
def get_public_key():
    """Retorna a chave pública RSA para criptografia no frontend"""
    return {"public_key": get_rsa_public_key_pem()}

@router.post("/login")
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Etapa 1 do login: autenticação de email e senha.
    Retorna instruções para o usuário inserir o código 2FA.
    """
    try:
        senha_decrypt = decrypt_rsa_password(login_data.senha)
        print(f"🔐 Senha descriptografada para {login_data.email}: {senha_decrypt}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Erro ao descriptografar senha: {str(e)}")

    # Buscar usuário baseado no tipo
    if login_data.tipo_usuario == "cliente":
        usuario = autenticar_cliente( login_data.email, senha_decrypt)
    elif login_data.tipo_usuario == "prestador":
        usuario = autenticar_prestador( login_data.email, senha_decrypt)
    else:
        raise HTTPException(status_code=400, detail="Tipo de usuário inválido")

    if not usuario:
        raise HTTPException(status_code=401, detail="Email ou senha incorretos")

    # Todos os usuários DEVEM ter 2FA configurado
    if not hasattr(usuario, 'totp_secret') or not usuario.totp_secret:
        raise HTTPException(
            status_code=403,
            detail="Este usuário não possui 2FA configurado. O login sem 2FA não é permitido."
        )

    print(f"✅ Etapa 1 concluída: {usuario.email} - aguardando código 2FA")

    return {
        "require_2fa": True,
        "tipo_usuario": login_data.tipo_usuario,
        "usuario_id": usuario.id,
        "email": usuario.email,
        "mensagem": "Insira o código de 2FA gerado no seu app autenticador para completar o login."
    }

@router.post("/login-2fa", response_model=LoginResponse)
def login_2fa(data: TwoFAVerifyRequest, db: Session = Depends(get_db)):
    """
    Etapa 2 do login: valida o código 2FA e emite o token de autenticação.
    """
    # Buscar usuário no DB
    if data.tipo_usuario == "cliente":
        usuario = buscar_cliente_por_email(db, data.email)
    elif data.tipo_usuario == "prestador":
        usuario = buscar_prestador_por_email(db, data.email)
    else:
        raise HTTPException(status_code=400, detail="Tipo de usuário inválido")

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Verifica se há segredo 2FA
    if not hasattr(usuario, 'totp_secret') or not usuario.totp_secret:
        raise HTTPException(status_code=403, detail="2FA não está configurado para este usuário")

    # Valida o código TOTP
    totp = pyotp.TOTP(usuario.totp_secret)
    if not totp.verify(data.codigo):
        raise HTTPException(status_code=401, detail="Código 2FA inválido")

    # Gera token de autenticação (idealmente JWT)
    token = f"token_{data.tipo_usuario}_{usuario.id}"

    print(f"✅ Login completo: {usuario.email} ({data.tipo_usuario})")

    return LoginResponse(
        token=token,
        tipo_usuario=data.tipo_usuario,
        usuario_id=usuario.id,
        nome=usuario.nome,
        email=usuario.email
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
    
    return PrestadorResponse(
        id=prestador.id,
        nome=prestador.nome,
        email=prestador.email,
        telefone=prestador.telefone,
        categorias=prestador.categorias,
        regioes_atendimento=prestador.regioes_atendimento,
        avaliacao_media=prestador.avaliacao_media,
        portfolio=prestador.portfolio,
        created_at=prestador.created_at
    )

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
    
    # Atualiza categorias no DB
    prestador.categorias = dados.categorias
    db.commit()
    
    return {"success": True, "message": "Categorias atualizadas com sucesso"}