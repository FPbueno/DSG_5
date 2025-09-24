# 📋 BACKLOG - Projeto ABP WorcaFlow

## 🎯 **VISÃO GERAL DO PROJETO**

**Objetivo:** Sistema completo de orçamentos com ML, autenticação segura e deploy em nuvem

**Arquitetura:** Híbrida - PostgreSQL (usuários) + Excel (dados ML)

**Status:** 60% concluído - Base técnica sólida, faltam segurança e deploy

---

## 🏷️ **ÉPICOS**

### 🔒 **ÉPICO 1: Segurança e Autenticação**

- **Descrição:** Implementar sistema completo de segurança e gestão de usuários
- **Prioridade:** 🔥 CRÍTICA

### ☁️ **ÉPICO 2: Deploy e Infraestrutura**

- **Descrição:** Hospedar aplicação na nuvem com segurança
- **Prioridade:** 🔥 CRÍTICA

### 🐳 **ÉPICO 3: Containerização e CI/CD**

- **Descrição:** Automatizar processos de desenvolvimento
- **Prioridade:** ⚠️ ALTA

### 🧪 **ÉPICO 4: Qualidade e Testes**

- **Descrição:** Garantir qualidade e confiabilidade
- **Prioridade:** ⚠️ ALTA

---

## 📋 **USER STORIES**

### 🔒 **ÉPICO 1: Segurança e Autenticação**

#### **US-001: Configurar HTTPS/TLS**

- **Como** desenvolvedor
- **Quero** implementar comunicação segura
- **Para que** os dados sejam protegidos em trânsito
- **Critérios de Aceitação:**
  - [ ] Certificado SSL para API
  - [ ] Configurar HTTPS no servidor
  - [ ] Atualizar URLs no Flutter para HTTPS
  - [ ] Testar comunicação segura
  - [ ] Forçar redirecionamento HTTP → HTTPS
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, Infraestrutura, Segurança

#### **US-002: Implementar PostgreSQL para Usuários**

- **Como** administrador do sistema
- **Quero** ter um banco de dados para usuários
- **Para que** possa gerenciar autenticação e permissões
- **Critérios de Aceitação:**
  - [ ] Configurar PostgreSQL para usuários
  - [ ] Criar schema de usuários e autenticação
  - [ ] Implementar sistema de roles e permissões
  - [ ] Manter dados ML no Excel (não migrar)
  - [ ] Configurar backup automático do banco de usuários
  - [ ] Implementar auditoria de ações dos usuários
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, Database, Segurança

#### **US-003: Criptografia de Usuários**

- **Como** usuário do sistema
- **Quero** que meus dados sejam criptografados
- **Para que** estejam protegidos contra acesso não autorizado
- **Critérios de Aceitação:**
  - [ ] Criptografia AES-256 para dados em repouso (PostgreSQL)
  - [ ] Criptografia TLS 1.3 para dados em trânsito
  - [ ] Chaves de criptografia rotativas
  - [ ] Validação de integridade dos dados
  - [ ] Criptografia de senhas com bcrypt (PostgreSQL)
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, Segurança, Database

#### **US-004: Sistema de Autenticação JWT**

- **Como** usuário
- **Quero** fazer login de forma segura
- **Para que** possa acessar o sistema com segurança
- **Critérios de Aceitação:**
  - [ ] Implementar JWT para autenticação
  - [ ] Sistema de refresh tokens
  - [ ] Middleware de autorização por roles
  - [ ] Controle de sessões ativas
  - [ ] Logout seguro e invalidação de tokens
  - [ ] Rate limiting por usuário
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, Segurança, Autenticação

#### **US-005: Validação e Sanitização**

- **Como** desenvolvedor
- **Quero** proteger contra ataques de injeção
- **Para que** o sistema seja seguro contra vulnerabilidades
- **Critérios de Aceitação:**
  - [ ] Validação de dados no backend (Pydantic)
  - [ ] Sanitização de inputs SQL injection
  - [ ] Validação no frontend
  - [ ] Mensagens de erro padronizadas
  - [ ] Validação de dados de usuário
- **Prioridade:** ⚠️ ALTA
- **Labels:** Backend, Frontend, Segurança

### ☁️ **ÉPICO 2: Deploy e Infraestrutura**

#### **US-006: Deploy da API na Nuvem**

- **Como** usuário final
- **Quero** acessar a aplicação na internet
- **Para que** possa usar o sistema de qualquer lugar
- **Critérios de Aceitação:**
  - [ ] Escolher plataforma (Heroku/Railway/Render)
  - [ ] Configurar variáveis de ambiente seguras
  - [ ] Deploy do backend com HTTPS
  - [ ] Configurar domínio personalizado
  - [ ] Testes de conectividade e segurança
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, Deploy, Infraestrutura

#### **US-007: Backup Seguro do PostgreSQL**

- **Como** administrador
- **Quero** ter backup seguro dos dados de usuários
- **Para que** não perca informações importantes
- **Critérios de Aceitação:**
  - [ ] Backup automático do PostgreSQL (usuários) na nuvem
  - [ ] Criptografia de backups do PostgreSQL
  - [ ] Controle de acesso aos backups
  - [ ] Validação de integridade dos backups
  - [ ] Logs de acesso aos dados
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, Segurança, Database

### 🐳 **ÉPICO 3: Containerização e CI/CD**

#### **US-008: Dockerfile para Flutter**

- **Como** desenvolvedor
- **Quero** containerizar a aplicação Flutter
- **Para que** seja fácil de deployar
- **Critérios de Aceitação:**
  - [ ] Criar Dockerfile para Flutter Web
  - [ ] Otimizar build para produção
  - [ ] Configurar nginx para servir arquivos
  - [ ] Testar container localmente
- **Prioridade:** ⚠️ ALTA
- **Labels:** Frontend, Docker, Deploy

#### **US-009: Docker Compose com PostgreSQL**

- **Como** desenvolvedor
- **Quero** orquestrar todos os serviços
- **Para que** a aplicação funcione de forma integrada
- **Critérios de Aceitação:**
  - [ ] Criar docker-compose.yml com PostgreSQL
  - [ ] Configurar rede entre containers
  - [ ] Volumes para persistência do banco de usuários
  - [ ] Volume para arquivo Excel (dados ML)
  - [ ] Variáveis de ambiente seguras
  - [ ] Scripts de inicialização do banco
- **Prioridade:** ⚠️ ALTA
- **Labels:** DevOps, Docker, Database

#### **US-010: Pipeline CI/CD Backend**

- **Como** desenvolvedor
- **Quero** automatizar o deploy do backend
- **Para que** as mudanças sejam aplicadas automaticamente
- **Critérios de Aceitação:**
  - [ ] Workflow de build e test
  - [ ] Deploy automático para produção
  - [ ] Testes automatizados
  - [ ] Notificações de status
- **Prioridade:** ⚠️ ALTA
- **Labels:** Backend, CI/CD, DevOps

#### **US-011: Pipeline CI/CD Frontend**

- **Como** desenvolvedor
- **Quero** automatizar o deploy do frontend
- **Para que** as mudanças sejam aplicadas automaticamente
- **Critérios de Aceitação:**
  - [ ] Build automático do Flutter
  - [ ] Deploy da versão web
  - [ ] Testes de widget
  - [ ] Versionamento automático
- **Prioridade:** ⚠️ ALTA
- **Labels:** Frontend, CI/CD, DevOps

### 🧪 **ÉPICO 4: Qualidade e Testes**

#### **US-012: Testes Backend e PostgreSQL**

- **Como** desenvolvedor
- **Quero** ter testes automatizados
- **Para que** a qualidade seja garantida
- **Critérios de Aceitação:**
  - [ ] Testes unitários dos serviços
  - [ ] Testes de integração da API
  - [ ] Testes dos modelos ML (Excel)
  - [ ] Testes de autenticação e autorização (PostgreSQL)
  - [ ] Testes de criptografia (PostgreSQL)
  - [ ] Coverage report
- **Prioridade:** 📝 MÉDIA
- **Labels:** Backend, Testes, Qualidade, Database

#### **US-013: Segurança Avançada**

- **Como** administrador
- **Quero** implementar proteções adicionais
- **Para que** o sistema seja ainda mais seguro
- **Critérios de Aceitação:**
  - [ ] Headers de segurança (CORS, CSP, HSTS)
  - [ ] Proteção contra ataques XSS
  - [ ] Validação rigorosa de dados
  - [ ] Configurar firewall básico
- **Prioridade:** ⚠️ ALTA
- **Labels:** Backend, Segurança, API

#### **US-014: Monitoramento e Logs**

- **Como** administrador
- **Quero** monitorar o sistema
- **Para que** possa detectar problemas rapidamente
- **Critérios de Aceitação:**
  - [ ] Rate limiting na API por usuário
  - [ ] Logs de segurança estruturados
  - [ ] Monitoramento de tentativas de login
  - [ ] Logs de ações dos usuários
  - [ ] Alertas automáticos de segurança
  - [ ] Detecção de atividades suspeitas
- **Prioridade:** ⚠️ ALTA
- **Labels:** Backend, Segurança, Monitoramento

---

## 📊 **SPRINT PLANNING**

### **SPRINT 1 - Fundação Segura Híbrida**

**Objetivo:** Aplicação segura com PostgreSQL (usuários) + Excel (dados ML)

**User Stories:**

- US-001: Configurar HTTPS/TLS
- US-002: Implementar PostgreSQL para Usuários
- US-003: Criptografia Híbrida
- US-004: Sistema de Autenticação JWT
- US-005: Validação e Sanitização
- US-006: Deploy da API na Nuvem
- US-007: Backup Seguro Híbrido

**Entregáveis:**

- API com HTTPS
- PostgreSQL (usuários) + Excel (ML)
- Autenticação JWT
- Criptografia completa
- Deploy em nuvem

#### **📦 ENTREGAS DA SPRINT 1:**

- ✅ **API com HTTPS/TLS** configurado e funcionando
- ✅ **PostgreSQL** configurado para usuários
- ✅ **Sistema de autenticação JWT** implementado
- ✅ **Criptografia de usuários** (senhas e dados sensíveis)
- ✅ **Validação e sanitização** de inputs
- ✅ **Deploy da API** em nuvem
- ✅ **Backup seguro** do PostgreSQL
- ✅ **Documentação** de segurança implementada

### **SPRINT 2 - Automação**

**Objetivo:** Processos automatizados

**User Stories:**

- US-008: Dockerfile para Flutter
- US-009: Docker Compose Híbrido
- US-010: Pipeline CI/CD Backend
- US-011: Pipeline CI/CD Frontend

**Entregáveis:**

- Docker completo
- CI/CD pipelines
- Automação de deploy

#### **📦 ENTREGAS DA SPRINT 2:**

- ✅ **Dockerfile para Flutter** criado e testado
- ✅ **Docker Compose** com PostgreSQL configurado
- ✅ **Pipeline CI/CD Backend** funcionando
- ✅ **Pipeline CI/CD Frontend** funcionando
- ✅ **Testes automatizados** implementados
- ✅ **Deploy automático** configurado
- ✅ **Containerização completa** da aplicação
- ✅ **Documentação** de deploy e CI/CD

### **SPRINT 3 - Excelência**

**Objetivo:** Segurança total + Qualidade

**User Stories:**

- US-012: Testes Híbridos
- US-013: Segurança Avançada
- US-014: Monitoramento e Logs

**Entregáveis:**

- Testes automatizados
- Segurança avançada
- Monitoramento completo

#### **📦 ENTREGAS DA SPRINT 3:**

- ✅ **Segurança avançada** implementada (headers, XSS, firewall)
- ✅ **Rate limiting** e logs de segurança
- ✅ **Sistema de logs** estruturado
- ✅ **Monitoramento** de atividades suspeitas
- ✅ **Testes finais** end-to-end completos
- ✅ **Otimização** de performance
- ✅ **Documentação técnica** completa
- ✅ **Verificação** de todos os requisitos

---

## 🎯 **DEFINITION OF DONE**

Para cada User Story ser considerada "Done":

- [ ] Código implementado e testado
- [ ] Pull request aprovado
- [ ] Deploy realizado (se aplicável)
- [ ] Documentação atualizada
- [ ] Testes passando
- [ ] Review de segurança (stories críticas)

---

## 📈 **MÉTRICAS DE PROGRESSO**

### **Por Épico:**

- 🔒 **Segurança e Autenticação:** 0/5 stories (0%)
- ☁️ **Deploy e Infraestrutura:** 0/2 stories (0%)
- 🐳 **Containerização e CI/CD:** 0/4 stories (0%)
- 🧪 **Qualidade e Testes:** 0/3 stories (0%)

### **Por Prioridade:**

- 🔥 **CRÍTICA:** 0/7 stories (0%)
- ⚠️ **ALTA:** 0/5 stories (0%)
- 📝 **MÉDIA:** 0/2 stories (0%)

### **Por Sprint:**

- **Sprint 1:** 0/7 stories (0%)
- **Sprint 2:** 0/4 stories (0%)
- **Sprint 3:** 0/3 stories (0%)

---

## 🏷️ **LABELS E TAGS**

### **Por Área:**

- 🔴 **Backend** - Desenvolvimento da API
- 🔵 **Frontend** - Desenvolvimento Flutter
- 🟡 **DevOps** - Infraestrutura e deploy
- 🟢 **ML** - Machine Learning
- 🟣 **Database** - Banco de dados
- 🔒 **Segurança** - Aspectos de segurança

### **Por Prioridade:**

- 🔥 **CRÍTICA** - Obrigatório para aprovação
- ⚠️ **ALTA** - Importante para qualidade
- 📝 **MÉDIA** - Desejável

### **Por Tipo:**

- 🚀 **Deploy** - Publicação e infraestrutura
- 🧪 **Testes** - Qualidade e validação
- 📚 **Documentação** - Docs e manuais
- 🔐 **Autenticação** - Sistema de usuários

---

## 📊 **CHECKLIST DE ENTREGA FINAL**

### **Para considerado COMPLETO:**

- [ ] **ML modelo funcionando em produção (Excel)**
- [ ] **API hospedada em nuvem e acessível**
- [ ] **App mobile funcionando**
- [ ] **Sistema de usuários (PostgreSQL)**
- [ ] **Dados protegidos com criptografia (PostgreSQL)**
- [ ] **Pipeline CI/CD ativo**
- [ ] **Containerização completa**

### **Mínimo para APROVAÇÃO:**

- [x] ✅ Modelo ML desenvolvido e treinado
- [x] ✅ API REST funcional
- [x] ✅ App mobile multiplataforma
- [ ] ❌ **Deploy em nuvem com HTTPS** (OBRIGATÓRIO)
- [ ] ❌ **PostgreSQL para usuários** (OBRIGATÓRIO)
- [ ] ❌ **Sistema de usuários e autenticação** (OBRIGATÓRIO)
- [ ] ❌ **Criptografia de usuários (PostgreSQL)** (OBRIGATÓRIO)
- [ ] ❌ **Docker completo** (OBRIGATÓRIO)
