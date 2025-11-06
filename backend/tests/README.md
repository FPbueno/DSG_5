# 🧪 Testes - WorcaFlow

Testes implementados seguindo as práticas de TDD e CI/CD.

## 📋 Estrutura

```
tests/
├── unit/              # Testes unitários (isolados)
├── integration/       # Testes de integração
├── fixtures/          # Fixtures compartilhadas (mocks, fakes)
│   ├── mock_data.py
│   └── fake_services.py
├── api/v1/           # Testes existentes (RSA, autenticação)
└── conftest.py       # Configurações globais
```

## 🚀 Executando os Testes

### Instalação

```bash
cd backend
pip install -r requirements.txt
```

### Executar Todos os Testes

```bash
pytest
```

### Executar Testes Específicos

```bash
# Por tipo
pytest -m unit          # Apenas unitários
pytest -m integration   # Apenas integração
pytest -m "not slow"    # Excluir lentos

# Por arquivo
pytest tests/api/v1/core/test_security_rsa.py

# Por função
pytest tests/api/v1/core/test_security_rsa.py::TestRSAGeneration::test_generate_rsa_keys_success
```

### Com Cobertura

```bash
# Cobertura completa
pytest --cov=api --cov-report=html --cov-report=term

# Ver relatório HTML
# Linux/Mac: open htmlcov/index.html
# Windows: start htmlcov/index.html

# Verificar cobertura mínima (70%)
pytest --cov=api --cov-fail-under=70
```

### Com Verbosidade

```bash
pytest -v              # Verboso
pytest -vv             # Muito verboso
pytest -s              # Mostrar prints
```

## ✅ Testes Implementados

### Testes Unitários

- ✅ **RSA/Segurança** (`test_security_rsa.py`)
  - Geração de chaves RSA
  - Formato da chave pública
  - Descriptografia de senhas
  - Tratamento de erros

### Testes de Integração

- ✅ **Endpoints RSA** (`test_rsa_endpoints.py`)
  - GET /api/v1/public-key
  - POST /api/v1/login com senha criptografada
  - Testes de segurança/penetração

### Em Desenvolvimento (DIA 2+)

- 🔄 **Orçamentos** - Characterization tests
- 🔄 **Solicitações** - Characterization tests
- 🔄 **Machine Learning** - Characterization tests
- 🔄 **Autenticação** - Expansão de testes

## 🎯 Cobertura Atual

- ✅ Geração de chaves RSA
- ✅ Endpoint de chave pública
- ✅ Descriptografia no login
- ✅ Tratamento de erros
- ✅ Testes de penetração/segurança

**Meta**: >70% de cobertura (em progresso)

## 📚 Documentação

Para mais detalhes sobre convenções e práticas de teste, consulte:

- [`TESTING.md`](../TESTING.md) - Guia completo de testes
- [`PLANO_TDD_CI_CD.md`](../../PLANO_TDD_CI_CD.md) - Plano de implementação

## 🔧 Fixtures Disponíveis

```python
# Fake services
def test_example(fake_supabase, fake_ml_service):
    # Usa fakes isolados
    pass

# Mock data
def test_example(mock_data):
    user_data = mock_data["user"]()
    orcamento_data = mock_data["orcamento"]()
    # ...
```

Veja [`TESTING.md`](../TESTING.md) para mais detalhes.

## 📊 CI/CD

Os testes são executados automaticamente via GitHub Actions em:

- Push para `main`, `develop`, `master`
- Pull Requests

Veja [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) para detalhes.
