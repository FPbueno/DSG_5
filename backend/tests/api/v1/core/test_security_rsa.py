"""
Testes unitários para criptografia RSA - Card SD-004, SD-005
"""
import pytest
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from api.v1.core.security import (
    generate_rsa_keys,
    get_rsa_public_key_pem,
    decrypt_rsa_password
)


class TestRSAGeneration:
    """Testes de geração de chaves RSA"""
    
    def test_generate_rsa_keys_success(self):
        """Testa geração bem-sucedida de chaves RSA"""
        private_key, public_key_pem = generate_rsa_keys()
        
        assert private_key is not None
        assert public_key_pem is not None
        assert isinstance(public_key_pem, str)
        assert "BEGIN PUBLIC KEY" in public_key_pem
        assert "END PUBLIC KEY" in public_key_pem
    
    def test_generate_rsa_keys_idempotent(self):
        """Testa que gerar chaves múltiplas vezes retorna as mesmas"""
        private_key1, public_key_pem1 = generate_rsa_keys()
        private_key2, public_key_pem2 = generate_rsa_keys()
        
        assert private_key1 is private_key2
        assert public_key_pem1 == public_key_pem2
    
    def test_get_public_key_pem_format(self):
        """Testa que a chave pública está em formato PEM válido"""
        public_key_pem = get_rsa_public_key_pem()
        
        assert public_key_pem is not None
        assert public_key_pem.startswith("-----BEGIN PUBLIC KEY-----")
        assert public_key_pem.endswith("-----END PUBLIC KEY-----\n")
        assert len(public_key_pem) > 200


class TestRSADecryption:
    """Testes de descriptografia RSA"""
    
    def test_decrypt_valid_password(self):
        """Testa descriptografia de senha válida"""
        # Gera chaves
        private_key, public_key_pem = generate_rsa_keys()
        public_key = private_key.public_key()
        
        # Criptografa uma senha de teste
        senha_original = "minhasenha123"
        senha_bytes = senha_original.encode('utf-8')
        
        encrypted = public_key.encrypt(
            senha_bytes,
            padding.PKCS1v15()
        )
        encrypted_base64 = base64.b64encode(encrypted).decode('utf-8')
        
        # Descriptografa
        senha_decrypt = decrypt_rsa_password(encrypted_base64)
        
        assert senha_decrypt == senha_original
    
    def test_decrypt_invalid_base64(self):
        """Testa erro ao descriptografar base64 inválido"""
        with pytest.raises(ValueError, match="Erro ao descriptografar senha"):
            decrypt_rsa_password("invalid_base64!!!")
    
    def test_decrypt_invalid_encrypted_data(self):
        """Testa erro ao descriptografar dados não criptografados"""
        invalid_data = base64.b64encode(b"not encrypted data").decode('utf-8')
        
        with pytest.raises(ValueError, match="Erro ao descriptografar senha"):
            decrypt_rsa_password(invalid_data)
    
    def test_decrypt_empty_password(self):
        """Testa descriptografia de senha vazia"""
        private_key, _ = generate_rsa_keys()
        public_key = private_key.public_key()
        
        senha_original = ""
        senha_bytes = senha_original.encode('utf-8')
        
        encrypted = public_key.encrypt(
            senha_bytes,
            padding.PKCS1v15()
        )
        encrypted_base64 = base64.b64encode(encrypted).decode('utf-8')
        
        senha_decrypt = decrypt_rsa_password(encrypted_base64)
        assert senha_decrypt == senha_original
    
    def test_decrypt_long_password(self):
        """Testa descriptografia de senha longa (limite RSA)"""
        private_key, _ = generate_rsa_keys()
        public_key = private_key.public_key()
        
        # RSA 2048 pode criptografar até ~245 bytes
        senha_original = "a" * 200
        senha_bytes = senha_original.encode('utf-8')
        
        encrypted = public_key.encrypt(
            senha_bytes,
            padding.PKCS1v15()
        )
        encrypted_base64 = base64.b64encode(encrypted).decode('utf-8')
        
        senha_decrypt = decrypt_rsa_password(encrypted_base64)
        assert senha_decrypt == senha_original


class TestRSASecurity:
    """Testes de segurança/penetração da criptografia E2E - Card SD-004"""
    
    def test_private_key_not_exposed(self):
        """Testa que a chave privada não é exposta publicamente"""
        public_key_pem = get_rsa_public_key_pem()
        
        assert "BEGIN PRIVATE KEY" not in public_key_pem
        assert "BEGIN RSA PRIVATE KEY" not in public_key_pem
    
    def test_same_message_different_encryption(self):
        """Testa que mesma mensagem gera criptografias diferentes (não determinística)"""
        private_key, _ = generate_rsa_keys()
        public_key = private_key.public_key()
        
        senha = "teste123"
        senha_bytes = senha.encode('utf-8')
        
        encrypted1 = public_key.encrypt(senha_bytes, padding.PKCS1v15())
        encrypted2 = public_key.encrypt(senha_bytes, padding.PKCS1v15())
        
        # Com PKCS1v15, as criptografias devem ser diferentes
        assert encrypted1 != encrypted2
    
    def test_public_key_structure(self):
        """Testa que a chave pública tem estrutura válida"""
        public_key_pem = get_rsa_public_key_pem()
        
        lines = public_key_pem.strip().split('\n')
        assert lines[0] == "-----BEGIN PUBLIC KEY-----"
        assert lines[-1] == "-----END PUBLIC KEY-----"
        assert len(lines) >= 3

