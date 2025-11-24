# 🧪 Guia de Testes - WorcaFlow

Este documento descreve as convenções e práticas de teste do projeto.

---

## 📋 **Índice**

1. [Estrutura de Testes](#estrutura-de-testes)
2. [Convenções de Nomenclatura](#convenções-de-nomenclatura)
3. [Padrão AAA](#padrão-aaa)
4. [Tipos de Testes](#tipos-de-testes)
5. [Mocks e Fixtures](#mocks-e-fixtures)
6. [Cobertura de Código](#cobertura-de-código)
7. [Executando Testes](#executando-testes)
8. [Definition of Done](#definition-of-done)

---

## 📁 **Estrutura de Testes**

```
backend/tests/
├── conftest.py              # Configurações globais do pytest
├── unit/                    # Testes unitários (isolados)
│   ├── api/v1/core/
│   ├── api/v1/services/
│   └── api/v1/models/
├── integration/             # Testes de integração
│   ├── api/v1/routes/
│   └── e2e/
├── fixtures/                # Fixtures compartilhadas
│   ├── mock_data.py        # Dados fake (Faker)
│   └── fake_services.py    # Fakes de serviços
└── README.md
```

### **Organização:**

- **`unit/`**: Testes que testam unidades isoladas (funções, classes, métodos)

  - Não dependem de banco de dados
  - Não dependem de rede
  - Não dependem de arquivos do sistema
  - Executam muito rápido

- **`integration/`**: Testes que testam múltiplas unidades trabalhando juntas

  - Podem usar mocks controlados
  - Testam fluxos completos
  - Podem depender de serviços fake

- **`fixtures/`**: Dados e serviços compartilhados
  - Factories de dados fake
  - Fakes de serviços (Supabase, ML, etc.)
  - Helpers para testes

---

## 🏷️ **Convenções de Nomenclatura**

### **Arquivos:**

```
test_<modulo>_<funcionalidade>.py
```

**Exemplos:**

- `test_auth_service.py` - Testes do serviço de autenticação
- `test_orcamento_creation.py` - Testes de criação de orçamento
- `test_ml_price_prediction.py` - Testes de predição de preços

### **Classes de Teste:**

```python
class Test<Modulo><Funcionalidade>:
    """Descrição do que está sendo testado"""
```

**Exemplos:**

```python
class TestAuthService:
    """Testes do serviço de autenticação"""

class TestOrcamentoCreation:
    """Testes de criação de orçamentos"""
```

### **Funções de Teste:**

```python
def test_<acao>_<condicao>_<resultado_esperado>():
    """Descrição clara do teste"""
```

**Exemplos:**

```python
def test_login_with_valid_credentials_returns_token():
    """Testa que login com credenciais válidas retorna token"""

def test_create_orcamento_with_invalid_data_raises_error():
    """Testa que criar orçamento com dados inválidos levanta erro"""
```

---

## 🎯 **Padrão AAA (Arrange, Act, Assert)**

Sempre organize seus testes no padrão AAA:

```python
def test_example():
    # ARRANGE - Preparar dados e ambiente
    user_data = create_fake_user_data()
    service = AuthService()

    # ACT - Executar ação sendo testada
    result = service.create_user(user_data)

    # ASSERT - Verificar resultado
    assert result is not None
    assert result["email"] == user_data["email"]
```

### **Exemplo Completo:**

```python
import pytest
from backend.tests.fixtures.mock_data import create_fake_user_data
from backend.api.v1.services.auth_service import AuthService

class TestAuthService:
    def test_create_user_success(self):
        # ARRANGE
        user_data = create_fake_user_data()
        service = AuthService()

        # ACT
        result = service.create_user(user_data)

        # ASSERT
        assert result is not None
        assert "id" in result
        assert result["email"] == user_data["email"]

    def test_create_user_with_duplicate_email_raises_error(self):
        # ARRANGE
        user_data = create_fake_user_data()
        service = AuthService()
        service.create_user(user_data)  # Primeiro usuário

        # ACT & ASSERT
        with pytest.raises(ValueError, match="Email já cadastrado"):
            service.create_user(user_data)  # Segundo usuário (duplicado)
```

---

## 📊 **Tipos de Testes**

### **1. Testes Unitários (`@pytest.mark.unit`)**

Testam unidades isoladas sem dependências externas.

```python
import pytest

@pytest.mark.unit
def test_validate_email_valid():
    """Testa validação de email válido"""
    from backend.api.v1.core.validators import validate_email

    assert validate_email("teste@example.com") == True
```

### **2. Testes de Integração (`@pytest.mark.integration`)**

Testam múltiplas unidades trabalhando juntas.

```python
@pytest.mark.integration
def test_create_solicitacao_flow():
    """Testa fluxo completo de criação de solicitação"""
    # Testa serviço + modelo + validação juntos
    ...
```

### **3. Testes E2E (`@pytest.mark.e2e`)**

Testam fluxos completos end-to-end.

```python
@pytest.mark.e2e
def test_fluxo_completo_solicitacao_orcamento():
    """Testa fluxo: solicitação → orçamento → aceite"""
    ...
```

### **4. Testes Lentos (`@pytest.mark.slow`)**

Testes que demoram para executar.

```python
@pytest.mark.slow
def test_ml_model_training():
    """Testa treinamento completo do modelo ML"""
    ...
```

**Executar apenas testes rápidos:**

```bash
pytest -m "not slow"
```

---

## 🎭 **Mocks e Fixtures**

### **Usando Fixtures do Pytest:**

```python
# conftest.py
import pytest
from backend.tests.fixtures.fake_services import FakeSupabaseService

@pytest.fixture
def fake_supabase():
    """Fixture que fornece fake do Supabase"""
    service = FakeSupabaseService()
    yield service
    service.clear()  # Limpa após teste
```

**Usando a fixture:**

```python
def test_create_user_with_fake_supabase(fake_supabase):
    """Testa criação de usuário usando fake do Supabase"""
    # ARRANGE
    service = AuthService(database=fake_supabase)
    user_data = create_fake_user_data()

    # ACT
    result = service.create_user(user_data)

    # ASSERT
    assert result is not None
```

### **Usando Mocks (pytest-mock):**

```python
from unittest.mock import Mock, patch

def test_ml_prediction_with_mock(mocker):
    """Testa predição de ML com mock"""
    # ARRANGE
    mock_ml_service = Mock()
    mock_ml_service.predict_price.return_value = 500.0

    # ACT
    result = some_function_that_uses_ml(mock_ml_service)

    # ASSERT
    assert result == 500.0
    mock_ml_service.predict_price.assert_called_once()
```

### **Dados Fake (Faker):**

```python
from backend.tests.fixtures.mock_data import (
    create_fake_user_data,
    create_fake_orcamento_data,
    create_fake_solicitacao_data
)

def test_example():
    user_data = create_fake_user_data()
    orcamento_data = create_fake_orcamento_data()
    # ...
```

---

## 📈 **Cobertura de Código**

### **Objetivos de Cobertura:**

- **Mínimo**: 70% nas unidades modificadas
- **Ideal**: 80%+ em todo o código
- **Crítico**: 90%+ (autenticação, pagamentos, ML)

### **Executar com Cobertura:**

```bash
# Cobertura completa
pytest --cov=api --cov-report=html --cov-report=term

# Ver relatório HTML
open htmlcov/index.html  # Linux/Mac
start htmlcov/index.html  # Windows
```

### **Verificar Cobertura Mínima:**

```bash
pytest --cov=api --cov-report=term --cov-fail-under=70
```

### **Excluir Linhas da Cobertura:**

```python
def some_function():
    # pragma: no cover
    if DEBUG_MODE:
        print("Debug info")
```

---

## 🚀 **Executando Testes**

### **Todos os Testes:**

```bash
cd backend
pytest
```

### **Testes Específicos:**

```bash
# Por arquivo
pytest tests/unit/api/v1/services/test_auth_service.py

# Por função
pytest tests/unit/api/v1/services/test_auth_service.py::TestAuthService::test_create_user

# Por marcador
pytest -m unit          # Apenas unitários
pytest -m integration   # Apenas integração
pytest -m "not slow"    # Excluir lentos
```

### **Com Verbosidade:**

```bash
pytest -v              # Verboso
pytest -vv             # Muito verboso
pytest -s              # Mostrar prints
```

### **Com Cobertura:**

```bash
pytest --cov=api --cov-report=html
```

### **Paralelo (mais rápido):**

```bash
pip install pytest-xdist
pytest -n auto  # Usa todos os CPUs disponíveis
```

---

## ✅ **Definition of Done (DoD)**

### **Para cada PR/Merge:**

- [ ] ✅ Todos os testes passando (`pytest`)
- [ ] ✅ Cobertura >70% nas unidades modificadas
- [ ] ✅ CI/CD pipeline verde
- [ ] ✅ Sem linter errors (flake8, black)
- [ ] ✅ Documentação atualizada
- [ ] ✅ Code review aprovado

### **Para cada Feature:**

- [ ] ✅ Testes unitários escritos (TDD quando possível)
- [ ] ✅ Testes de integração para fluxos críticos
- [ ] ✅ Documentação de API atualizada
- [ ] ✅ Exemplos de uso

### **Para cada Bugfix:**

- [ ] ✅ Teste que reproduz o bug (RED)
- [ ] ✅ Teste passando após correção (GREEN)
- [ ] ✅ Refatoração se necessário (REFACTOR)

---

## 🎓 **Boas Práticas**

### **✅ FAZER:**

1. **Um assert por teste** (quando possível)

   ```python
   def test_something():
       result = function()
       assert result.status == "success"
       assert result.code == 200
   ```

2. **Testes independentes** (sem ordem)

   ```python
   # Cada teste deve funcionar isoladamente
   def test_a(): ...
   def test_b(): ...  # Não depende de test_a
   ```

3. **Nomes descritivos**

   ```python
   # ✅ BOM
   def test_login_with_invalid_password_raises_error():

   # ❌ RUIM
   def test_login():
   ```

4. **Usar fixtures para setup comum**

   ```python
   @pytest.fixture
   def user_service():
       return UserService()
   ```

5. **Mockar dependências externas**
   ```python
   # Mockar Supabase, HTTP, arquivos
   ```

### **❌ EVITAR:**

1. **Testes que dependem uns dos outros**

   ```python
   # ❌ RUIM - test_b depende de test_a
   def test_a():
       global x
       x = 1

   def test_b():
       assert x == 1  # Falha se test_a não rodar primeiro
   ```

2. **Testes muito complexos**

   ```python
   # ❌ RUIM - testa muitas coisas
   def test_everything():
       # 100 linhas de código...
   ```

3. **Dados hardcoded**

   ```python
   # ❌ RUIM
   email = "teste@teste.com"

   # ✅ BOM
   user_data = create_fake_user_data()
   email = user_data["email"]
   ```

4. **Ignorar testes que falham**
   ```python
   # ❌ RUIM
   @pytest.mark.skip(reason="Não funciona")
   def test_something(): ...
   ```

---

## 📚 **Recursos**

- [pytest documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Testing Best Practices](https://realpython.com/python-testing/)
- [TDD Guide](https://martinfowler.com/bliki/TestDrivenDevelopment.html)

---

**Última atualização**: 2025-01-XX
