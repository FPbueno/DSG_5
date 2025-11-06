# 📋 PLANO DE IMPLEMENTAÇÃO TDD, CI E CD

## Roteiro de 7 Dias para o Projeto WorcaFlow

---

## 🎯 **VISÃO GERAL DO PROJETO ATUAL**

### **Estado Atual:**

- ✅ **Backend**: FastAPI com estrutura organizada
- ✅ **Frontend**: Flutter multiplataforma
- ✅ **Testes**: Alguns testes de RSA/criptografia já existem
- ✅ **Frameworks**: pytest configurado no backend
- ❌ **CI/CD**: Ainda não configurado
- ⚠️ **Cobertura**: Testes apenas para módulo de segurança

### **Módulos Principais Identificados:**

1. **Autenticação** (auth.py, auth_service.py) - PARCIALMENTE TESTADO
2. **Orçamentos** (orcamentos.py, orcamento_service.py) - NÃO TESTADO
3. **Solicitações** (solicitacoes.py, solicitacao_service.py) - NÃO TESTADO
4. **Clientes** (clients.py) - NÃO TESTADO
5. **Serviços** (services.py) - NÃO TESTADO
6. **Machine Learning** (ml.py, ml_service.py) - NÃO TESTADO
7. **Avaliações** (avaliacoes.py, avaliacao_service.py) - NÃO TESTADO
8. **Analytics** (analytics.py) - NÃO TESTADO
9. **Usuários** (usuarios.py, user_service.py) - NÃO TESTADO

---

## 📅 **ROTEIRO DE IMPLEMENTAÇÃO - 7 DIAS**

---

## **DIA 1: DIAGNÓSTICO E SETUP DO AMBIENTE** ✅

### **Objetivos:**

- [x] Mapear módulos críticos do projeto
- [ ] Instalar/verificar frameworks de teste
- [ ] Configurar CI/CD (GitHub Actions)
- [ ] Criar estrutura de testes organizada
- [ ] Documentar convenções de teste

### **Ações a Realizar:**

#### 1.1 **Verificar Frameworks de Teste**

```bash
# Backend - Python
✅ pytest já instalado
✅ pytest-asyncio já instalado
✅ httpx para testes HTTP já instalado
❌ pytest-cov (coverage) - PRECISA INSTALAR
❌ pytest-mock - PRECISA INSTALAR
```

#### 1.2 **Configurar CI/CD com GitHub Actions**

- Criar workflow `.github/workflows/ci.yml`
- Configurar testes automáticos no push/PR
- Adicionar badge de status no README

#### 1.3 **Estrutura de Testes Proposta**

```
backend/tests/
├── conftest.py                 # ✅ JÁ EXISTE
├── unit/                       # ❌ CRIAR
│   ├── api/v1/core/
│   ├── api/v1/services/
│   └── api/v1/models/
├── integration/                # ❌ CRIAR
│   ├── api/v1/routes/
│   └── e2e/
└── fixtures/                   # ❌ CRIAR
    ├── mock_data.py
    └── fake_services.py
```

#### 1.4 **Documentar Convenções**

- Naming: `test_*.py`, `Test*`
- Padrão AAA: Arrange, Act, Assert
- Uso de mocks/fixtures
- DoD (Definition of Done)

---

## **DIA 2: CHARACTERIZATION TESTS** 🔍

### **Objetivos:**

- Capturar comportamento atual dos módulos
- Criar rede de segurança antes de refatorar
- Isolar dependências externas (Supabase, arquivos, ML models)

### **Módulos Prioritários para Characterization Tests:**

#### 2.1 **Orçamentos (OrçamentoService)**

- Testar criação, leitura, atualização, exclusão
- Capturar comportamento atual com Supabase
- Testar integração com ML para previsão de preços

#### 2.2 **Solicitações (SolicitacaoService)**

- Testar fluxo completo de solicitação
- Validar estados e transições
- Testar integração com orçamentos

#### 2.3 **Machine Learning (MLService)**

- Testar predição de preços (snapshot/golden file)
- Testar predição de categorias
- Validar fallback quando modelos não carregam

#### 2.4 **Autenticação (AuthService)**

- Testar login/registro com Supabase
- Validar geração de JWT tokens
- Testar criptografia de senhas

### **Estratégia:**

- Usar **snapshots** para outputs de ML
- Usar **golden files** para respostas de API
- **Mockar Supabase** para evitar dependências externas

---

## **DIA 3: PORTS, ADAPTERS E INJEÇÃO DE DEPENDÊNCIAS** 🔌

### **Objetivos:**

- Extrair dependências para interfaces (Ports)
- Criar Adapters reais e Fakes para testes
- Permitir testes sem acesso a rede/disco/Supabase

### **Refatorações Necessárias:**

#### 3.1 **SupabaseService → Interface**

```python
# Port (interface)
class DatabasePort(ABC):
    @abstractmethod
    async def create_user(self, user_data): pass

    @abstractmethod
    async def get_user_by_email(self, email): pass

# Adapter Real
class SupabaseAdapter(DatabasePort):
    # Implementação real com Supabase

# Adapter Fake (para testes)
class FakeDatabaseAdapter(DatabasePort):
    # Implementação em memória
```

#### 3.2 **MLService → Interface**

```python
# Port
class MLPort(ABC):
    @abstractmethod
    def predict_price(self, description: str) -> float: pass

# Adapter Real
class SklearnMLAdapter(MLPort):
    # Carrega modelos .pkl

# Adapter Fake
class FakeMLAdapter(MLPort):
    # Retorna valores fixos para testes
```

#### 3.3 **FileService → Interface**

```python
# Para ExcelService e arquivos de modelos
class FileStoragePort(ABC):
    @abstractmethod
    def read_file(self, path: str): pass

# Adapter Fake
class InMemoryFileAdapter(FileStoragePort):
    # Simula leitura de arquivos
```

### **Benefícios:**

- ✅ Testes sem depender de Supabase
- ✅ Testes sem arquivos reais
- ✅ Testes mais rápidos
- ✅ Maior isolamento

---

## **DIA 4: PRIMEIRA HISTÓRIA EM TDD** 🧪

### **Objetivos:**

- Escolher uma feature pequena
- Aplicar ciclo Red → Green → Refactor
- Validar abordagem TDD

### **Feature Sugerida: "Validação de Email"**

#### Ciclo TDD:

1. **RED**: Escrever teste que falha

   ```python
   def test_validate_email_valid():
       assert validate_email("teste@example.com") == True

   def test_validate_email_invalid():
       assert validate_email("email-invalido") == False
   ```

2. **GREEN**: Implementar mínimo necessário

   ```python
   def validate_email(email: str) -> bool:
       return "@" in email and "." in email.split("@")[1]
   ```

3. **REFACTOR**: Melhorar código mantendo testes verdes

   ```python
   import re

   def validate_email(email: str) -> bool:
       pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
       return bool(re.match(pattern, email))
   ```

### **Outras Features Pequenas para TDD:**

- Validação de CPF/CNPJ
- Formatação de telefone
- Cálculo de preço com desconto
- Validação de status de orçamento

---

## **DIA 5: REFATORAÇÕES SEGURAS** 🔧

### **Objetivos:**

- Aplicar refactorings com testes de apoio
- Reduzir acoplamento
- Extrair funções e serviços
- Melhorar legibilidade

### **Refatorações Propostas:**

#### 5.1 **Extrair Lógica de Negócio**

- Mover validações de rotas para services
- Extrair cálculos complexos
- Separar concerns (separação de responsabilidades)

#### 5.2 **Reduzir Duplicação**

- Identificar código duplicado
- Extrair métodos comuns
- Criar helpers/utils

#### 5.3 **Melhorar Nomes e Estrutura**

- Renomear variáveis/funções ambíguas
- Reorganizar imports
- Adicionar type hints

#### 5.4 **Metas de Cobertura**

- **Objetivo**: >70% de cobertura nas unidades
- Focar em lógica de negócio crítica
- Priorizar services sobre rotas

---

## **DIA 6: INTEGRAÇÃO E E2E** 🔗

### **Objetivos:**

- Criar testes de contrato entre módulos
- Automatizar cenários end-to-end
- Validar fluxos críticos de negócio

### **Testes de Integração:**

#### 6.1 **Fluxo Completo: Solicitação → Orçamento → Aceite**

```python
def test_fluxo_completo_solicitacao_orcamento():
    # 1. Cliente cria solicitação
    solicitacao = criar_solicitacao(...)

    # 2. Prestador envia orçamento
    orcamento = criar_orcamento(solicitacao_id=...)

    # 3. Cliente aceita orçamento
    orcamento_aceito = aceitar_orcamento(orcamento_id=...)

    # 4. Validar estado final
    assert orcamento_aceito.status == "aceito"
```

#### 6.2 **Testes de Contrato**

- Validar formato de responses
- Validar schemas Pydantic
- Testar compatibilidade entre versões

#### 6.3 **Testes E2E com TestClient**

- Testar endpoints completos
- Validar autenticação/autorização
- Testar error handling

#### 6.4 **Mutation Testing (Opcional)**

- Introduzir em área piloto
- Validar qualidade dos testes

---

## **DIA 7: NORMAS, MÉTRICAS E EXPANSÃO** 📊

### **Objetivos:**

- Formalizar Definition of Done (DoD)
- Definir políticas de cobertura
- Planejar expansão gradual
- Criar dashboard de qualidade

### **Definition of Done (DoD):**

#### Para cada PR/Merge:

- [ ] Todos os testes passando
- [ ] Cobertura >70% nas unidades modificadas
- [ ] CI/CD pipeline verde
- [ ] Sem linter errors
- [ ] Documentação atualizada
- [ ] Code review aprovado

#### Para cada Feature:

- [ ] Testes unitários escritos (TDD)
- [ ] Testes de integração para fluxos críticos
- [ ] Documentação de API atualizada
- [ ] Exemplos de uso

### **Políticas:**

#### Cobertura:

- **Mínimo**: 70% nas unidades
- **Ideal**: 80%+
- **Crítico**: 90%+ (autenticação, pagamentos)

#### Mocks:

- Sempre mockar dependências externas (Supabase, HTTP, arquivos)
- Usar fixtures para dados de teste
- Evitar testes que dependem de estado global

#### Convenções:

- Naming: `test_<funcionalidade>_<cenario>`
- AAA: Arrange, Act, Assert
- Um assert por teste quando possível
- Testes independentes (sem ordem)

### **Dashboard de Qualidade:**

- Badge de status CI/CD no README
- Cobertura de código (codecov)
- Testes passando/falhando
- Métricas de qualidade (sonarcloud)

### **Plano de Expansão:**

1. **Semana 1-2**: Backend (services e routes)
2. **Semana 3**: ML e Analytics
3. **Semana 4**: Frontend (Flutter/Dart)
4. **Semana 5+**: E2E completo e otimizações

---

## 🛠️ **FERRAMENTAS E DEPENDÊNCIAS**

### **Backend (Python):**

```txt
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-cov>=4.0.0          # Coverage
pytest-mock>=3.10.0        # Mocks avançados
httpx>=0.24.0              # TestClient HTTP
faker>=18.0.0              # Dados falsos para testes
```

### **CI/CD:**

- GitHub Actions (gratuito)
- Codecov (cobertura)
- SonarCloud (qualidade)

### **Frontend (Flutter):**

```yaml
dev_dependencies:
  flutter_test: # ✅ Já existe
  mockito: ^5.4.0 # Mocks
  integration_test: # Testes E2E
```

---

## 📈 **MÉTRICAS DE SUCESSO**

### **Curto Prazo (7 dias):**

- ✅ CI/CD configurado e rodando
- ✅ Characterization tests para módulos críticos
- ✅ Ports & Adapters implementados
- ✅ Primeira feature em TDD completa
- ✅ Cobertura >50% no backend

### **Médio Prazo (1 mês):**

- ✅ Cobertura >70% no backend
- ✅ Testes E2E para fluxos críticos
- ✅ DoD formalizado e aplicado
- ✅ Dashboard de qualidade ativo

### **Longo Prazo (3 meses):**

- ✅ Cobertura >80% em todo projeto
- ✅ Testes E2E completos
- ✅ Frontend testado (Flutter)
- ✅ CD (Continuous Deployment) configurado

---

## 🚀 **PRÓXIMOS PASSOS IMEDIATOS**

1. **Instalar dependências de teste**
2. **Configurar GitHub Actions**
3. **Criar estrutura de testes**
4. **Começar com characterization tests**

---

## 📚 **RECURSOS E REFERÊNCIAS**

- [pytest documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Flutter Testing](https://docs.flutter.dev/testing)
- [GitHub Actions](https://docs.github.com/en/actions)
- [TDD Best Practices](https://martinfowler.com/bliki/TestDrivenDevelopment.html)

---

**Pronto para começar? Vamos implementar passo a passo!** 🎯
