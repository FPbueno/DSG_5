"""
Dados mock e factories para testes
"""
from faker import Faker
from typing import Dict, Any

fake = Faker('pt_BR')


def create_fake_user_data() -> Dict[str, Any]:
    """Cria dados fake de usuário"""
    return {
        "nome": fake.name(),
        "email": fake.email(),
        "senha": fake.password(length=12),
        "telefone": fake.phone_number(),
        "tipo_usuario": fake.random_element(elements=("cliente", "prestador")),
    }


def create_fake_client_data() -> Dict[str, Any]:
    """Cria dados fake de cliente"""
    return {
        "nome": fake.name(),
        "email": fake.email(),
        "telefone": fake.phone_number(),
        "endereco": fake.address(),
    }


def create_fake_solicitacao_data() -> Dict[str, Any]:
    """Cria dados fake de solicitação"""
    return {
        "descricao": fake.text(max_nb_chars=200),
        "categoria": fake.random_element(elements=(
            "Limpeza", "Pintura", "Encanamento", "Elétrica", "Jardim"
        )),
        "endereco": fake.address(),
        "urgencia": fake.random_element(elements=("baixa", "media", "alta")),
    }


def create_fake_orcamento_data() -> Dict[str, Any]:
    """Cria dados fake de orçamento"""
    return {
        "valor": float(fake.random_int(min=100, max=5000)),
        "prazo": fake.random_int(min=1, max=30),
        "descricao": fake.text(max_nb_chars=200),
        "status": fake.random_element(elements=("pendente", "aceito", "recusado")),
    }


def create_fake_service_data() -> Dict[str, Any]:
    """Cria dados fake de serviço"""
    return {
        "nome": fake.job(),
        "descricao": fake.text(max_nb_chars=200),
        "categoria": fake.random_element(elements=(
            "Limpeza", "Pintura", "Encanamento", "Elétrica", "Jardim"
        )),
        "preco_base": float(fake.random_int(min=50, max=1000)),
    }

