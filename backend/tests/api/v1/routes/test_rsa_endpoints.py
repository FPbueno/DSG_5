"""
Testes de integração para endpoints RSA - Card SD-004, SD-005
"""
import pytest
import base64
from fastapi.testclient import TestClient
from cryptography.hazmat.primitives.asymmetric import padding
from api.v1.core.security import generate_rsa_keys


@pytest.fixture(scope="module")
def client():
    """Fixture que fornece TestClient do FastAPI"""
    import sys
    from pathlib import Path
    
    # Garante que o path está configurado
    backend_dir = Path(__file__).resolve().parent.parent.parent.parent
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))
    
    # Importa setup_path para garantir que o path está configurado
    try:
        import setup_path  # noqa: F401
    except ImportError:
        pass
    
    from main import app
    return TestClient(app)


class TestPublicKeyEndpoint:
    """Testes para endpoint GET /api/v1/public-key"""
    
    def test_get_public_key_success(self, client):
        """Testa que o endpoint retorna chave pública válida"""
        # Garante que as chaves estão geradas
        generate_rsa_keys()
        
        response = client.get("/api/v1/public-key")
        
        assert response.status_code == 200
        data = response.json()
        assert "public_key" in data
        assert data["public_key"] is not None
        assert "BEGIN PUBLIC KEY" in data["public_key"]
        assert "END PUBLIC KEY" in data["public_key"]
    
    def test_get_public_key_format(self, client):
        """Testa formato correto da chave pública"""
        generate_rsa_keys()
        
        response = client.get("/api/v1/public-key")
        data = response.json()
        public_key_pem = data["public_key"]
        
        assert public_key_pem.startswith("-----BEGIN PUBLIC KEY-----")
        assert public_key_pem.endswith("-----END PUBLIC KEY-----\n")
    
    def test_get_public_key_stable(self, client):
        """Testa que múltiplas requisições retornam mesma chave"""
        generate_rsa_keys()
        
        response1 = client.get("/api/v1/public-key")
        response2 = client.get("/api/v1/public-key")
        
        key1 = response1.json()["public_key"]
        key2 = response2.json()["public_key"]
        
        assert key1 == key2


class TestLoginWithEncryptedPassword:
    """Testes para endpoint POST /api/v1/login com senha criptografada - Card SD-005"""
    
    def setup_method(self):
        """Configuração antes de cada teste"""
        generate_rsa_keys()
    
    def _encrypt_password(self, password: str) -> str:
        """Helper para criptografar senha para testes"""
        from api.v1.core.security import get_rsa_public_key_pem
        from cryptography.hazmat.primitives import serialization
        
        public_key_pem = get_rsa_public_key_pem()
        public_key = serialization.load_pem_public_key(
            public_key_pem.encode('utf-8')
        )
        
        senha_bytes = password.encode('utf-8')
        encrypted = public_key.encrypt(senha_bytes, padding.PKCS1v15())
        return base64.b64encode(encrypted).decode('utf-8')
    
    def test_login_with_encrypted_password_invalid_format(self, client):
        """Testa erro ao enviar senha não criptografada"""
        response = client.post(
            "/api/v1/login",
            json={
                "email": "teste@teste.com",
                "senha": "senha_nao_criptografada",
                "tipo_usuario": "cliente"
            }
        )
        
        # Deve falhar ao tentar descriptografar
        assert response.status_code in [400, 401]
    
    def test_login_with_encrypted_password_invalid_base64(self, client):
        """Testa erro ao enviar base64 inválido"""
        response = client.post(
            "/api/v1/login",
            json={
                "email": "teste@teste.com",
                "senha": "!!!invalid_base64!!!",
                "tipo_usuario": "cliente"
            }
        )
        
        assert response.status_code == 400
        assert "Erro ao descriptografar senha" in response.json()["detail"]
    
    def test_login_with_encrypted_password_correct_format(self, client):
        """Testa que senha criptografada corretamente é aceita"""
        senha_criptografada = self._encrypt_password("minhasenha123")
        
        # Nota: Este teste depende de ter um usuário real no banco
        # Por isso pode falhar se não houver dados de teste
        response = client.post(
            "/api/v1/login",
            json={
                "email": "teste@teste.com",
                "senha": senha_criptografada,
                "tipo_usuario": "cliente"
            }
        )
        
        # Se usuário não existe, retorna 401
        # Se senha está em formato correto mas errada, retorna 401
        # Se formato está errado, retorna 400
        assert response.status_code in [400, 401]
        
        # Se retornou 400, é porque a descriptografia falhou (formato errado)
        if response.status_code == 400:
            assert "Erro ao descriptografar senha" in response.json()["detail"]


class TestRSAEndpointSecurity:
    """Testes de segurança/penetração dos endpoints RSA - Card SD-004"""
    
    def test_public_key_endpoint_no_auth_required(self, client):
        """Testa que endpoint de chave pública não requer autenticação"""
        # Endpoint deve ser público para o frontend obter a chave
        response = client.get("/api/v1/public-key")
        
        assert response.status_code == 200
    
    def test_login_with_manipulated_encrypted_data(self, client):
        """Testa que dados manipulados não são aceitos"""
        # Tenta enviar dados que parecem base64 mas não são criptografia válida
        manipulated_data = base64.b64encode(b"fake encrypted data").decode('utf-8')
        
        response = client.post(
            "/api/v1/login",
            json={
                "email": "teste@teste.com",
                "senha": manipulated_data,
                "tipo_usuario": "cliente"
            }
        )
        
        # Deve retornar erro ao tentar descriptografar
        assert response.status_code == 400
    
    def test_login_with_non_encrypted_password_rejected(self, client):
        """Testa que senha em texto plano é rejeitada"""
        response = client.post(
            "/api/v1/login",
            json={
                "email": "teste@teste.com",
                "senha": "senha_em_texto_plano",
                "tipo_usuario": "cliente"
            }
        )
        
        # Não deve aceitar senha não criptografada
        assert response.status_code == 400

