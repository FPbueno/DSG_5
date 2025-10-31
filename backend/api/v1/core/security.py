from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import base64
import os
from dotenv import load_dotenv

load_dotenv('config.env')

# Configurações de segurança
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Configurações de criptografia
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "your-encryption-key-32-chars-long")
IV_LENGTH = int(os.getenv("IV_LENGTH", "16"))

# Contexto para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Chaves RSA para criptografia de ponta a ponta
_rsa_private_key = None
_rsa_public_key_pem = None

def generate_rsa_keys():
    """Gera par de chaves RSA para criptografia de ponta a ponta"""
    global _rsa_private_key, _rsa_public_key_pem
    try:
        if _rsa_private_key is None:
            _rsa_private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            _rsa_public_key = _rsa_private_key.public_key()
            _rsa_public_key_pem_bytes = _rsa_public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            _rsa_public_key_pem = _rsa_public_key_pem_bytes.decode('utf-8')
        return _rsa_private_key, _rsa_public_key_pem
    except Exception as e:
        print(f"Erro ao gerar chaves RSA: {e}")
        raise

def get_rsa_public_key_pem() -> str:
    """Retorna a chave pública RSA em formato PEM"""
    if _rsa_public_key_pem is None:
        generate_rsa_keys()
    if _rsa_public_key_pem is None:
        raise RuntimeError("Chave pública RSA não foi gerada corretamente")
    return _rsa_public_key_pem

def decrypt_rsa_password(encrypted_password: str) -> str:
    """Descriptografa senha usando chave privada RSA"""
    if _rsa_private_key is None:
        generate_rsa_keys()
    try:
        encrypted_bytes = base64.b64decode(encrypted_password)
        # Usa PKCS1v15 que é compatível com a biblioteca encrypt do Dart
        decrypted_password = _rsa_private_key.decrypt(
            encrypted_bytes,
            padding.PKCS1v15()
        )
        return decrypted_password.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Erro ao descriptografar senha: {str(e)}")

# Configurar chave de criptografia
def get_encryption_key():
    """Gera ou recupera chave de criptografia"""
    key = ENCRYPTION_KEY.encode()
    if len(key) < 32:
        key = key.ljust(32, b'0')
    elif len(key) > 32:
        key = key[:32]
    return base64.urlsafe_b64encode(key)

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """Cria token JWT"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Gera hash da senha"""
    return pwd_context.hash(password)

def encrypt_data(data: str) -> str:
    """Criptografa dados"""
    key = get_encryption_key()
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return base64.urlsafe_b64encode(encrypted_data).decode()

def decrypt_data(encrypted_data: str) -> str:
    """Descriptografa dados"""
    key = get_encryption_key()
    f = Fernet(key)
    decoded_data = base64.urlsafe_b64decode(encrypted_data.encode())
    decrypted_data = f.decrypt(decoded_data)
    return decrypted_data.decode()

def verify_token(token: str) -> Union[str, None]:
    """Verifica e decodifica token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except jwt.JWTError:
        return None
