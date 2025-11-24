"""
Testes TDD para Validadores
Ciclo: Red -> Green -> Refactor
"""
import pytest
from api.v1.core.validators import validate_email, validate_phone, validate_cpf


@pytest.mark.unit
class TestValidateEmailTDD:
    """Testes TDD para validação de email"""
    
    def test_validate_email_valid_format(self):
        """Testa email válido"""
        # ARRANGE
        email = "teste@example.com"
        
        # ACT
        resultado = validate_email(email)
        
        # ASSERT
        assert resultado is True
    
    def test_validate_email_invalid_format_no_at(self):
        """Testa email sem @"""
        # ARRANGE
        email = "testeexample.com"
        
        # ACT
        resultado = validate_email(email)
        
        # ASSERT
        assert resultado is False
    
    def test_validate_email_invalid_format_no_domain(self):
        """Testa email sem domínio"""
        # ARRANGE
        email = "teste@"
        
        # ACT
        resultado = validate_email(email)
        
        # ASSERT
        assert resultado is False
    
    def test_validate_email_invalid_format_no_tld(self):
        """Testa email sem TLD"""
        # ARRANGE
        email = "teste@example"
        
        # ACT
        resultado = validate_email(email)
        
        # ASSERT
        assert resultado is False
    
    def test_validate_email_valid_with_special_chars(self):
        """Testa email válido com caracteres especiais"""
        # ARRANGE
        email = "teste.user+tag@example-domain.co.uk"
        
        # ACT
        resultado = validate_email(email)
        
        # ASSERT
        assert resultado is True
    
    def test_validate_email_empty_string(self):
        """Testa email vazio"""
        # ARRANGE
        email = ""
        
        # ACT
        resultado = validate_email(email)
        
        # ASSERT
        assert resultado is False
    
    def test_validate_email_none(self):
        """Testa email None"""
        # ARRANGE
        email = None
        
        # ACT
        resultado = validate_email(email)
        
        # ASSERT
        assert resultado is False


@pytest.mark.unit
class TestValidatePhoneTDD:
    """Testes TDD para validação de telefone"""
    
    def test_validate_phone_format_1(self):
        """Testa telefone formato (11) 99999-9999"""
        # ARRANGE
        phone = "(11) 99999-9999"
        
        # ACT
        resultado = validate_phone(phone)
        
        # ASSERT
        assert resultado is True
    
    def test_validate_phone_format_2(self):
        """Testa telefone formato 11999999999"""
        # ARRANGE
        phone = "11999999999"
        
        # ACT
        resultado = validate_phone(phone)
        
        # ASSERT
        assert resultado is True
    
    def test_validate_phone_format_3(self):
        """Testa telefone formato (11) 9999-9999"""
        # ARRANGE
        phone = "(11) 9999-9999"
        
        # ACT
        resultado = validate_phone(phone)
        
        # ASSERT
        assert resultado is True
    
    def test_validate_phone_invalid_too_short(self):
        """Testa telefone muito curto"""
        # ARRANGE
        phone = "12345"
        
        # ACT
        resultado = validate_phone(phone)
        
        # ASSERT
        assert resultado is False
    
    def test_validate_phone_empty(self):
        """Testa telefone vazio"""
        # ARRANGE
        phone = ""
        
        # ACT
        resultado = validate_phone(phone)
        
        # ASSERT
        assert resultado is False


@pytest.mark.unit
class TestValidateCPFTDD:
    """Testes TDD para validação de CPF"""
    
    def test_validate_cpf_formatted(self):
        """Testa CPF formatado"""
        # ARRANGE
        cpf = "123.456.789-00"
        
        # ACT
        resultado = validate_cpf(cpf)
        
        # ASSERT
        assert resultado is True
    
    def test_validate_cpf_unformatted(self):
        """Testa CPF sem formatação"""
        # ARRANGE
        cpf = "12345678900"
        
        # ACT
        resultado = validate_cpf(cpf)
        
        # ASSERT
        assert resultado is True
    
    def test_validate_cpf_invalid_too_short(self):
        """Testa CPF muito curto"""
        # ARRANGE
        cpf = "123456789"
        
        # ACT
        resultado = validate_cpf(cpf)
        
        # ASSERT
        assert resultado is False
    
    def test_validate_cpf_invalid_all_same_digits(self):
        """Testa CPF com todos dígitos iguais"""
        # ARRANGE
        cpf = "111.111.111-11"
        
        # ACT
        resultado = validate_cpf(cpf)
        
        # ASSERT
        assert resultado is False
    
    def test_validate_cpf_empty(self):
        """Testa CPF vazio"""
        # ARRANGE
        cpf = ""
        
        # ACT
        resultado = validate_cpf(cpf)
        
        # ASSERT
        assert resultado is False

