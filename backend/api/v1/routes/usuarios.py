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
from ..services.auth_service_supabase import ( 
    criar_cliente, criar_prestador,
    autenticar_cliente, autenticar_prestador,
    buscar_cliente_por_email, buscar_prestador_por_email,
    buscar_prestador_por_id
)
from ..core.security import get_rsa_public_key_pem, decrypt_rsa_password
from api.v1.schemas.usuarios import TwoFAVerifyRequest
import pyotp
import qrcode
import io
import base64
from api.v1.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# ============= 2FA UTILS =============

def gerar_2fa_secret(email: str, tipo_usuario: str, nome: str = None):
    """Gera segredo TOTP e QR Code para configuração no app autenticador"""
    totp_secret = pyotp.random_base32()
    
    # Gera o URI TOTP no formato padrão
    # otpauth://totp/Issuer:Label?secret=SECRET&issuer=Issuer
    issuer = "WorcaFlow"
    label = f"{issuer}:{email}" if nome is None else f"{issuer}:{nome} ({email})"
    totp_uri = pyotp.totp.TOTP(totp_secret).provisioning_uri(
        name=label,
        issuer_name=issuer
    )
    
    # Gera QR Code em base64
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(totp_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    qr_code_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    qr_code_data_url = f"data:image/png;base64,{qr_code_base64}"
    
    print(f"🔐 Segredo 2FA gerado: {totp_secret}")
    
    return {
        "secret": totp_secret,
        "qr_code": qr_code_data_url,
        "uri": totp_uri
    }

# ============= TESTE =============

@router.post("/teste")
def teste_endpoint(dados: dict):
    """Endpoint de teste para debugar"""
    print(f"🔍 Dados brutos recebidos: {dados}")
    return {"message": "Dados recebidos com sucesso", "dados": dados}

# ============= REGISTRO =============

@router.post("/registrar", response_model=RegistrarClienteResponse)
def registrar_cliente(cliente_data: ClienteCreate, db: Session = Depends(get_db)):
    """Registra novo cliente com 2FA (usando Supabase)"""
    if buscar_cliente_por_email(cliente_data.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Gerar segredo 2FA com QR Code
    totp_data = gerar_2fa_secret(cliente_data.email, "cliente", cliente_data.nome)
    totp_secret = totp_data["secret"]

    # Descriptografa a senha recebida (vem criptografada do front-end)
    senha_plain = decrypt_rsa_password(cliente_data.senha)
    
    # Substitua a senha no cliente_data com a plain (o criar_cliente fará o hash)
    cliente_data.senha = senha_plain

    # Criar cliente via Supabase (passando cliente_data e totp_secret)
    cliente = criar_cliente(cliente_data, totp_secret)
    if not cliente:
        raise HTTPException(status_code=500, detail="Erro ao criar cliente")

    # O totp_secret já é incluído no cliente pelo criar_cliente
    # cliente é um dict retornado do Supabase (não precisa de db.commit())

    return {
        "cliente": ClienteResponse(
            id=cliente["id"],
            nome=cliente["nome"],
            email=cliente["email"],
            telefone=cliente["telefone"],
            endereco=cliente["endereco"],
            avaliacao_media=cliente.get("avaliacao_media", 0.0) or 0.0, 
            created_at=cliente["created_at"]
        ),
        "codigo_2fa": totp_secret,
        "qr_code": totp_data["qr_code"],
        "mensagem": "Escaneie o QR Code com seu app autenticador (Google Authenticator, Authy etc.) para ativar o 2FA, ou digite manualmente o código secreto."
    }

@router.post(
    "/prestadores/registrar",
    response_model=PrestadorRegistroResponse,
    status_code=status.HTTP_201_CREATED
)
def registrar_prestador(prestador_data: PrestadorCreate, db: Session = Depends(get_db)):
    if buscar_prestador_por_email(prestador_data.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    totp_data = gerar_2fa_secret(prestador_data.email, "prestador", prestador_data.nome)
    secret = totp_data["secret"]
    
    # Mesmo processo: descriptografar
    senha_plain = decrypt_rsa_password(prestador_data.senha)
    prestador_data.senha = senha_plain
    prestador_data.totp_secret = secret

    prestador = criar_prestador(prestador_data)
    if not prestador:
        raise HTTPException(status_code=500, detail="Erro ao criar prestador")

    return {
        "prestador": PrestadorResponse(
            id=prestador["id"],
            nome=prestador["nome"],
            email=prestador["email"],
            telefone=prestador["telefone"],
            categorias=prestador["categorias"],
            regioes_atendimento=prestador["regioes_atendimento"],
            avaliacao_media=prestador.get("avaliacao_media", 0.0) or 0.0,
            portfolio=prestador.get("portfolio", ""),
            created_at=prestador["created_at"]
        ),
        "codigo_2fa": secret,
        "qr_code": totp_data["qr_code"],
        "mensagem": "Escaneie o QR Code com seu app autenticador (Google Authenticator, Authy etc.) para ativar o 2FA, ou digite manualmente o código secreto."
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
    # usuario é um dict retornado do Supabase
    if not usuario.get('totp_secret'):
        raise HTTPException(
            status_code=403,
            detail="Este usuário não possui 2FA configurado. O login sem 2FA não é permitido."
        )

    print(f"✅ Etapa 1 concluída: {usuario['email']} - aguardando código 2FA")

    return {
        "require_2fa": True,
        "tipo_usuario": login_data.tipo_usuario,
        "usuario_id": usuario["id"],
        "email": usuario["email"],
        "mensagem": "Insira o código de 2FA gerado no seu app autenticador para completar o login."
    }

@router.post("/login-2fa", response_model=LoginResponse)
def login_2fa(data: TwoFAVerifyRequest, db: Session = Depends(get_db)):
    """
    Etapa 2 do login: valida o código 2FA e emite o token de autenticação.
    """
    # Buscar usuário no DB
    if data.tipo_usuario == "cliente":
        usuario = buscar_cliente_por_email(data.email)
    elif data.tipo_usuario == "prestador":
        usuario = buscar_prestador_por_email(data.email)
    else:
        raise HTTPException(status_code=400, detail="Tipo de usuário inválido")

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Verifica se há segredo 2FA
    # usuario é um dict retornado do Supabase
    totp_secret = usuario.get('totp_secret')
    if not totp_secret:
        raise HTTPException(status_code=403, detail="2FA não está configurado para este usuário")

    # Valida o código TOTP
    totp = pyotp.TOTP(totp_secret)
    if not totp.verify(data.codigo):
        raise HTTPException(status_code=401, detail="Código 2FA inválido")

    # Gera token de autenticação (idealmente JWT)
    token = f"token_{data.tipo_usuario}_{usuario['id']}"

    print(f"✅ Login completo: {usuario['email']} ({data.tipo_usuario})")

    return LoginResponse(
        token=token,
        tipo_usuario=data.tipo_usuario,
        usuario_id=usuario["id"],
        nome=usuario["nome"],
        email=usuario["email"]
    )

# ============= GESTÃO DE PRESTADORES =============

@router.get("/prestadores/{prestador_id}", response_model=PrestadorResponse)
def buscar_prestador(prestador_id: int, db: Session = Depends(get_db)):
    """Busca dados do prestador"""
    prestador = buscar_prestador_por_id(prestador_id)
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
    prestador = buscar_prestador_por_id(prestador_id)
    if not prestador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prestador não encontrado"
        )
    
    # Atualiza categorias no DB
    prestador.categorias = dados.categorias
    db.commit()
    
    return {"success": True, "message": "Categorias atualizadas com sucesso"}