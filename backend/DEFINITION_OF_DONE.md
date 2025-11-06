# ✅ Definition of Done (DoD)

## WorcaFlow - Critérios de Conclusão

---

## 📋 **Para cada PR/Merge**

### ✅ Checklist Obrigatório

- [ ] ✅ **Todos os testes passando**

  ```bash
  pytest
  ```

- [ ] ✅ **Cobertura >70% nas unidades modificadas**

  ```bash
  pytest --cov=api --cov-fail-under=70
  ```

- [ ] ✅ **CI/CD pipeline verde**

  - Verificar status no GitHub Actions
  - Todos os jobs devem passar

- [ ] ✅ **Sem linter errors**

  ```bash
  flake8 api
  black --check api
  ```

- [ ] ✅ **Documentação atualizada**

  - README atualizado se necessário
  - Docstrings em funções/métodos novos
  - Comentários em código complexo

- [ ] ✅ **Code review aprovado**
  - Pelo menos 1 aprovação
  - Comentários resolvidos

---

## 📋 **Para cada Feature**

### ✅ Checklist Obrigatório

- [ ] ✅ **Testes unitários escritos (TDD quando possível)**

  - Testes antes ou junto com implementação
  - Cobertura adequada da funcionalidade

- [ ] ✅ **Testes de integração para fluxos críticos**

  - Testes E2E se aplicável
  - Validação de integração entre módulos

- [ ] ✅ **Documentação de API atualizada**

  - Schemas Pydantic documentados
  - Endpoints documentados (FastAPI auto-doc)
  - Exemplos de uso

- [ ] ✅ **Exemplos de uso**
  - Exemplos no README ou documentação
  - Testes servem como exemplos

---

## 📋 **Para cada Bugfix**

### ✅ Checklist Obrigatório

- [ ] ✅ **Teste que reproduz o bug (RED)**

  - Teste que falha antes da correção

- [ ] ✅ **Teste passando após correção (GREEN)**

  - Teste deve passar com a correção

- [ ] ✅ **Refatoração se necessário (REFACTOR)**
  - Melhorar código se necessário
  - Manter testes verdes

---

## 📊 **Políticas de Cobertura**

### **Mínimo: 70% nas unidades**

- Aplicado a código novo ou modificado
- Verificado via CI/CD

### **Ideal: 80%+**

- Meta para código crítico
- Focar em lógica de negócio

### **Crítico: 90%+**

- Autenticação
- Pagamentos
- Processamento de dados sensíveis
- ML predictions

---

## 🎯 **Políticas de Mocks**

### ✅ **Sempre mockar dependências externas:**

- Supabase/banco de dados
- APIs externas
- Serviços de rede
- Sistema de arquivos

### ✅ **Usar fixtures para dados de teste:**

- Factories de dados fake (Faker)
- Fixtures compartilhadas
- Evitar dados hardcoded

### ✅ **Evitar testes que dependem de estado global:**

- Testes independentes
- Setup/teardown adequado
- Não depender de ordem de execução

---

## 🔍 **Code Quality**

### **Linting:**

- Flake8 sem erros críticos
- Black para formatação (opcional mas recomendado)

### **Type Hints:**

- Adicionar type hints em código novo
- Melhorar gradualmente código existente

### **Documentação:**

- Docstrings em funções/métodos públicos
- Comentários em lógica complexa
- README atualizado

---

## 📈 **Métricas de Sucesso**

### **Cobertura de Código:**

- ✅ Mínimo: 70%
- 🎯 Ideal: 80%+
- 🏆 Crítico: 90%+

### **Velocidade dos Testes:**

- ✅ Testes unitários: <1s cada
- ✅ Testes integração: <5s cada
- ✅ Testes E2E: <30s cada

### **CI/CD:**

- ✅ Pipeline completa: <10 minutos
- ✅ Feedback rápido para desenvolvedores

---

## 🚀 **Como Verificar DoD**

### **Localmente:**

```bash
# Testes
pytest

# Cobertura
pytest --cov=api --cov-report=html

# Linting
flake8 api
black --check api
```

### **No CI/CD:**

- Verificar status no GitHub Actions
- Revisar relatório de cobertura
- Verificar badges no README

---

**Última atualização**: 2025-01-XX  
**Aplicável a**: Todo código novo ou modificado
