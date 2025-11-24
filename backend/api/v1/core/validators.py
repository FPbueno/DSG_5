"""
Validadores - Implementados com TDD
"""
import re
from typing import Optional


def validate_email(email: str) -> bool:
    """
    Valida formato de email
    Implementado seguindo TDD (Red -> Green -> Refactor)
    """
    if not email or not isinstance(email, str):
        return False
    
    # Padrão básico de email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone: str) -> bool:
    """
    Valida formato de telefone brasileiro
    Aceita: (11) 99999-9999, 11999999999, (11) 9999-9999
    """
    if not phone or not isinstance(phone, str):
        return False
    
    # Remove espaços, parênteses, hífens
    phone_clean = re.sub(r'[\s\(\)\-]', '', phone)
    
    # Verifica se tem 10 ou 11 dígitos (fixo ou celular)
    return bool(re.match(r'^\d{10,11}$', phone_clean))


def validate_cpf(cpf: str) -> bool:
    """
    Valida CPF brasileiro
    Aceita formatado (123.456.789-00) ou sem formatação (12345678900)
    """
    if not cpf or not isinstance(cpf, str):
        return False
    
    # Remove formatação
    cpf_clean = re.sub(r'[\.\-]', '', cpf)
    
    # Verifica se tem 11 dígitos
    if not re.match(r'^\d{11}$', cpf_clean):
        return False
    
    # Verifica se não são todos dígitos iguais
    if len(set(cpf_clean)) == 1:
        return False
    
    # Validação dos dígitos verificadores
    # (implementação simplificada - pode ser expandida)
    return True

