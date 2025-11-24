"""
Characterization Tests para Auth Service
"""
import pytest
from unittest.mock import patch, MagicMock
from api.v1.services.auth_service_supabase import (
    hash_senha,
    verificar_senha,
    criar_cliente,
    autenticar_cliente,
    criar_prestador,
    autenticar_prestador
)
from api.v1.schemas import ClienteCreate, PrestadorCreate


@pytest.mark.unit
class TestAuthServiceCharacterization:
    """Testes de caracterização do serviço de autenticação"""
    
    def test_hash_senha_gera_hash_diferente(self):
        """Testa que hash de senha é diferente da senha original"""
        # ARRANGE
        senha = "minhasenha123"
        
        # ACT
        hash1 = hash_senha(senha)
        hash2 = hash_senha(senha)
        
        # ASSERT - Captura comportamento: bcrypt gera hash diferente a cada vez
        assert hash1 != senha
        assert hash2 != senha
        # Hash deve começar com prefixo bcrypt
        assert hash1.startswith("$bcrypt")
        assert hash2.startswith("$bcrypt")
    
    def test_verificar_senha_valida_corretamente(self):
        """Testa verificação de senha"""
        # ARRANGE
        senha = "minhasenha123"
        hash_correto = hash_senha(senha)
        
        # ACT
        resultado_correto = verificar_senha(senha, hash_correto)
        resultado_incorreto = verificar_senha("senhaerrada", hash_correto)
        
        # ASSERT
        assert resultado_correto is True
        assert resultado_incorreto is False
    
    def test_criar_cliente_estrutura(self):
        """Testa estrutura de criação de cliente"""
        # ARRANGE
        cliente_data = ClienteCreate(
            nome="João Silva",
            email="joao@teste.com",
            senha="senha123",
            telefone="11999999999",
            endereco="Rua Teste, 123"
        )
        
        # ACT
        with patch('api.v1.services.auth_service_supabase.supabase_service') as mock_supabase:
            mock_supabase.supabase.table.return_value.insert.return_value.execute.return_value = MagicMock(
                data=[{
                    "id": 1,
                    "nome": "João Silva",
                    "email": "joao@teste.com"
                }]
            )
            resultado = criar_cliente(cliente_data)
        
        # ASSERT
        assert resultado is not None
        assert isinstance(resultado, dict)
        assert resultado["nome"] == "João Silva"
        assert resultado["email"] == "joao@teste.com"
        # Senha não deve estar no resultado
        assert "senha" not in resultado
        assert "senha_hash" not in resultado  # Hash não retornado no create
    
    def test_autenticar_cliente_sucesso(self):
        """Testa autenticação bem-sucedida"""
        # ARRANGE
        email = "joao@teste.com"
        senha = "senha123"
        hash_senha_cliente = hash_senha(senha)
        
        # ACT
        with patch('api.v1.services.auth_service_supabase.buscar_cliente_por_email') as mock_buscar:
            mock_buscar.return_value = {
                "id": 1,
                "email": email,
                "senha_hash": hash_senha_cliente
            }
            resultado = autenticar_cliente(email, senha)
        
        # ASSERT
        assert resultado is not None
        assert resultado["email"] == email
    
    def test_autenticar_cliente_senha_incorreta(self):
        """Testa autenticação com senha incorreta"""
        # ARRANGE
        email = "joao@teste.com"
        senha_errada = "senhaerrada"
        hash_senha_cliente = hash_senha("senhacorreta")
        
        # ACT
        with patch('api.v1.services.auth_service_supabase.buscar_cliente_por_email') as mock_buscar:
            mock_buscar.return_value = {
                "id": 1,
                "email": email,
                "senha_hash": hash_senha_cliente
            }
            resultado = autenticar_cliente(email, senha_errada)
        
        # ASSERT
        assert resultado is None
    
    def test_criar_prestador_estrutura(self):
        """Testa estrutura de criação de prestador"""
        # ARRANGE
        prestador_data = PrestadorCreate(
            nome="Empresa XYZ",
            email="empresa@teste.com",
            senha="senha123",
            telefone="11999999999",
            cpf_cnpj="12345678901",
            categorias=["Pintura", "Limpeza"],
            regioes_atendimento=["São Paulo"],
            portfolio=[{"descricao": "Portfolio teste"}]
        )
        
        # ACT
        with patch('api.v1.services.auth_service_supabase.supabase_service') as mock_supabase:
            mock_supabase.criar_prestador.return_value = {
                "id": 1,
                "nome": "Empresa XYZ",
                "email": "empresa@teste.com",
                "avaliacao_media": 0.0
            }
            resultado = criar_prestador(prestador_data)
        
        # ASSERT
        assert resultado is not None
        assert isinstance(resultado, dict)
        assert resultado["nome"] == "Empresa XYZ"
        assert resultado["avaliacao_media"] == 0.0

