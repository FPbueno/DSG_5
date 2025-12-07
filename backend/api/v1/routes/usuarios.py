"""
Rotas de Autenticação e Gestão de Usuários (Clientes e Prestadores)
"""
from fastapi import APIRouter, HTTPException, status, Depends
from ..schemas import (
    ClienteCreate, ClienteResponse,
    PrestadorCreate, PrestadorResponse,
    LoginRequest, LoginResponse, RegistrarClienteResponse, PrestadorRegistroResponse
)
from ..services.auth_service_supabase import (
    criar_cliente, criar_prestador,
    autenticar_cliente, autenticar_prestador,
    buscar_cliente_por_email, buscar_prestador_por_email,
    buscar_prestador_por_id,
)
from ..services.supabase_service import supabase_service
from ..core.security import get_rsa_public_key_pem, decrypt_rsa_password
from ..schemas.usuarios import TwoFAVerifyRequest
from pydantic import BaseModel
import pyotp
import qrcode
import io
import base64
import secrets
import json
from ..core.database import get_db
from sqlalchemy.orm import Session
from ..services.auth_service_supabase import hash_senha, verificar_senha

router = APIRouter()

# ============= 2FA UTILS =============

def gerar_backup_codes(quantidade: int = 10) -> list[str]:
    """Gera códigos de backup únicos para recuperação 2FA"""
    codes = []
    for _ in range(quantidade):
        # Formato: XXXX-XXXX-XXXX (12 caracteres alfanuméricos)
        code = f"{secrets.token_hex(2).upper()}-{secrets.token_hex(2).upper()}-{secrets.token_hex(2).upper()}"
        codes.append(code)
    return codes

def hash_backup_codes(codes: list[str]) -> list[str]:
    """Gera hash dos backup codes para armazenamento seguro"""
    return [hash_senha(code) for code in codes]

def verificar_backup_code(codigo: str, backup_codes_hashed: list) -> bool:
    """Verifica se um backup code é válido"""
    if not backup_codes_hashed or not isinstance(backup_codes_hashed, list):
        return False
    
    for code_hash in backup_codes_hashed:
        if verificar_senha(codigo, code_hash):
            return True
    return False

def remover_backup_code_usado(codigo: str, backup_codes_hashed: list) -> list:
    """Remove um backup code usado da lista"""
    if not backup_codes_hashed or not isinstance(backup_codes_hashed, list):
        return []
    
    return [code_hash for code_hash in backup_codes_hashed 
            if not verificar_senha(codigo, code_hash)]

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
    """Registra novo cliente com 2FA e backup codes (usando Supabase)"""
    if buscar_cliente_por_email(cliente_data.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Gerar segredo 2FA com QR Code
    totp_data = gerar_2fa_secret(cliente_data.email, "cliente", cliente_data.nome)
    totp_secret = totp_data["secret"]

    # Gerar backup codes
    backup_codes = gerar_backup_codes(10)
    backup_codes_hashed = hash_backup_codes(backup_codes)

    # Descriptografa a senha recebida (vem criptografada do front-end)
    senha_plain = decrypt_rsa_password(cliente_data.senha)
    
    # Substitua a senha no cliente_data com a plain (o criar_cliente fará o hash)
    cliente_data.senha = senha_plain

    # Criar cliente via Supabase (passando cliente_data, totp_secret e backup_codes)
    cliente = criar_cliente(cliente_data, totp_secret, backup_codes_hashed)
    if not cliente:
        raise HTTPException(status_code=500, detail="Erro ao criar cliente")

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
        "backup_codes": backup_codes,
        "mensagem": "Escaneie o QR Code com seu app autenticador (Google Authenticator, Authy etc.) para ativar o 2FA, ou digite manualmente o código secreto. Salve os códigos de backup em local seguro."
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
    
    # Gerar backup codes
    backup_codes = gerar_backup_codes(10)
    backup_codes_hashed = hash_backup_codes(backup_codes)
    
    # Mesmo processo: descriptografar
    senha_plain = decrypt_rsa_password(prestador_data.senha)
    prestador_data.senha = senha_plain
    prestador_data.totp_secret = secret

    prestador = criar_prestador(prestador_data, backup_codes_hashed)
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
            portfolio=prestador.get("portfolio") or [],
            created_at=prestador["created_at"]
        ),
        "codigo_2fa": secret,
        "qr_code": totp_data["qr_code"],
        "backup_codes": backup_codes,
        "mensagem": "Escaneie o QR Code com seu app autenticador (Google Authenticator, Authy etc.) para ativar o 2FA, ou digite manualmente o código secreto. Salve os códigos de backup em local seguro."
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
    Etapa 2 do login: valida o código 2FA (TOTP ou backup code) e emite o token de autenticação.
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
    totp_secret = usuario.get('totp_secret')
    if not totp_secret:
        raise HTTPException(status_code=403, detail="2FA não está configurado para este usuário")

    codigo_valido = False
    backup_codes = usuario.get('backup_codes', [])
    
    # Remove espaços e normaliza o código
    codigo_limpo = data.codigo.replace(' ', '').strip()
    codigo_sem_hifen = codigo_limpo.replace('-', '').upper()
    
    # Tenta validar como código TOTP (6 dígitos)
    if len(codigo_sem_hifen) == 6 and codigo_sem_hifen.isdigit():
        totp = pyotp.TOTP(totp_secret)
        codigo_valido = totp.verify(codigo_sem_hifen)
    
    # Se não for TOTP válido, tenta como backup code
    if not codigo_valido:
        # Backup codes têm formato XXXX-XXXX-XXXX (12 caracteres hexadecimais)
        if len(codigo_sem_hifen) == 12 and all(c in '0123456789ABCDEF' for c in codigo_sem_hifen):
            # Normaliza para formato com hífens
            if '-' not in codigo_limpo:
                # Adiciona hífens se não tiver
                codigo_backup = f"{codigo_sem_hifen[:4]}-{codigo_sem_hifen[4:8]}-{codigo_sem_hifen[8:12]}"
            else:
                codigo_backup = codigo_limpo.upper()
            codigo_valido = verificar_backup_code(codigo_backup, backup_codes)
            
            # Se backup code válido, remove da lista
            if codigo_valido:
                backup_codes_atualizados = remover_backup_code_usado(codigo_backup, backup_codes)
                # Atualiza no banco
                if data.tipo_usuario == "cliente":
                    supabase_service.supabase.table("clientes").update({
                        "backup_codes": backup_codes_atualizados
                    }).eq("id", usuario["id"]).execute()
                else:
                    supabase_service.supabase.table("prestadores").update({
                        "backup_codes": backup_codes_atualizados
                    }).eq("id", usuario["id"]).execute()
                print(f"🔑 Backup code usado e removido: {usuario['email']}")

    if not codigo_valido:
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

# ============= BACKUP CODES =============

class RegenerarBackupCodesRequest(BaseModel):
    email: str
    tipo_usuario: str

class RegenerarBackupCodesResponse(BaseModel):
    backup_codes: list[str]
    mensagem: str

@router.post("/regenerar-backup-codes", response_model=RegenerarBackupCodesResponse)
def regenerar_backup_codes(data: RegenerarBackupCodesRequest, db: Session = Depends(get_db)):
    """
    Regenera backup codes para um usuário. 
    IMPORTANTE: Os códigos antigos são invalidados.
    """
    # Buscar usuário
    if data.tipo_usuario == "cliente":
        usuario = buscar_cliente_por_email(data.email)
    elif data.tipo_usuario == "prestador":
        usuario = buscar_prestador_por_email(data.email)
    else:
        raise HTTPException(status_code=400, detail="Tipo de usuário inválido")

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not usuario.get('totp_secret'):
        raise HTTPException(status_code=403, detail="2FA não está configurado para este usuário")

    # Gerar novos backup codes
    backup_codes = gerar_backup_codes(10)
    backup_codes_hashed = hash_backup_codes(backup_codes)

    # Atualizar no banco
    if data.tipo_usuario == "cliente":
        supabase_service.supabase.table("clientes").update({
            "backup_codes": backup_codes_hashed
        }).eq("id", usuario["id"]).execute()
    else:
        supabase_service.supabase.table("prestadores").update({
            "backup_codes": backup_codes_hashed
        }).eq("id", usuario["id"]).execute()

    print(f"🔑 Backup codes regenerados: {usuario['email']} ({data.tipo_usuario})")

    return RegenerarBackupCodesResponse(
        backup_codes=backup_codes,
        mensagem="Novos códigos de backup gerados. Os códigos antigos foram invalidados. Salve estes códigos em local seguro."
    )

# ============= GESTÃO DE PRESTADORES =============

@router.get("/prestadores/{prestador_id}", response_model=PrestadorResponse)
def buscar_prestador(prestador_id: int):
    """Busca dados do prestador"""
    prestador = buscar_prestador_por_id(prestador_id)
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
    prestador = buscar_prestador_por_id(prestador_id)
    if not prestador:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prestador não encontrado",
        )

    try:
        resp = (
            supabase_service.get_client()
            .table("prestadores")
            .update({"categorias": dados.categorias})
            .eq("id", prestador_id)
            .execute()
        )
        if not resp.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao atualizar categorias do prestador",
            )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao atualizar categorias do prestador: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar categorias do prestador",
        )

    return {"success": True, "message": "Categorias atualizadas com sucesso"}