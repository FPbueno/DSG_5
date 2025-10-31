# Testes de Criptografia E2E

Testes implementados conforme Cards SD-004 e SD-005 do Trello.

## Executando os Testes

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar todos os testes
pytest

# Executar testes específicos
pytest tests/api/v1/core/test_security_rsa.py
pytest tests/api/v1/routes/test_rsa_endpoints.py

# Executar com verbosidade
pytest -v

# Executar com coverage
pytest --cov=api --cov-report=html
```

## Testes Implementados

### Testes Unitários (test_security_rsa.py)

- Geração de chaves RSA
- Formato da chave pública
- Descriptografia de senhas válidas
- Tratamento de erros (base64 inválido, dados não criptografados)
- Testes de segurança/penetração

### Testes de Integração (test_rsa_endpoints.py)

- Endpoint GET /api/v1/public-key
- Endpoint POST /api/v1/login com senha criptografada
- Testes de segurança/penetração dos endpoints

## Cobertura

Testes cobrem:

- ✅ Geração de chaves RSA
- ✅ Endpoint de chave pública
- ✅ Descriptografia no login
- ✅ Tratamento de erros
- ✅ Testes de penetração/segurança
