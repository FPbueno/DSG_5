# 📋 BACKLOG DO PROJETO ABP - WorkFlow

## 📊 Visão Geral do Projeto

**Objetivo:** Desenvolver uma aplicação completa de Machine Learning com interface mobile, API segura e deploy em nuvem, utilizando MySQL para dados de aplicação.

**Arquitetura:** Flutter (Frontend) + FastAPI (Backend) + MySQL (Dados) + Modelos ML (.pkl)

---

## 🏃‍♂️ SPRINT 1 - Fundação Segura e Deploy Básico

### 🎯 Objetivo do Sprint

Estabelecer a base segura da aplicação com autenticação, criptografia e deploy inicial em nuvem.

### 📋 User Stories

#### US001 - Configuração HTTPS/TLS

**Como** desenvolvedor  
**Eu quero** implementar comunicação segura HTTPS/TLS  
**Para que** a aplicação tenha segurança na transmissão de dados

**Critérios de Aceitação:**

- [ ] Certificado SSL configurado para API
- [ ] HTTPS habilitado no servidor
- [ ] URLs do Flutter atualizadas para HTTPS
- [ ] Comunicação segura testada e funcionando
- [ ] Redirecionamento HTTP → HTTPS implementado

**Prioridade:** 🔥 CRÍTICA  
**Story Points:** 8  
**Labels:** Backend, Infraestrutura, Segurança

---

#### US002 - Implementar Banco MySQL para Dados ✅

**Como** desenvolvedor  
**Eu quero** configurar MySQL para dados de usuários e transações  
**Para que** os dados sejam armazenados de forma segura e estruturada

**Critérios de Aceitação:**

- [x] MySQL configurado para a aplicação
- [x] Schema de usuários e autenticação criado
- [x] Sistema de roles e permissões implementado (tipo_usuario)
- [x] Modelos ML mantidos separados (arquivos .pkl)
- [ ] Backup automático do banco configurado
- [ ] Auditoria de ações dos usuários implementada

**Prioridade:** 🔥 CRÍTICA  
**Story Points:** 13  
**Labels:** Backend, Database, Segurança  
**Status:** ✅ CONCLUÍDO (Parcialmente - Backup e Auditoria pendentes)

---

#### US003 - Criptografia de Dados de Usuários ⚠️

**Como** desenvolvedor  
**Eu quero** implementar criptografia robusta para dados de usuários no MySQL  
**Para que** informações sensíveis sejam protegidas mesmo em caso de vazamento

**Critérios de Aceitação:**

- [ ] Criptografia AES-256 para dados em repouso
- [ ] Criptografia TLS 1.3 para dados em trânsito
- [ ] Sistema de chaves de criptografia rotativas
- [x] Validação de integridade dos dados (Pydantic)
- [x] Criptografia de senhas com bcrypt

**Prioridade:** 🔥 CRÍTICA  
**Story Points:** 8  
**Labels:** Backend, Segurança, Database  
**Status:** ⚠️ EM ANDAMENTO (Senhas OK, TLS pendente)

---

#### US004 - Sistema de Autenticação e Autorização ⚠️

**Como** usuário  
**Eu quero** um sistema seguro de login e controle de acesso  
**Para que** apenas usuários autorizados acessem funcionalidades específicas

**Critérios de Aceitação:**

- [ ] JWT implementado para autenticação
- [ ] Sistema de refresh tokens funcional
- [x] Middleware de autorização por roles (tipo_usuario)
- [ ] Controle de sessões ativas
- [ ] Logout seguro e invalidação de tokens
- [ ] Rate limiting por usuário

**Prioridade:** 🔥 CRÍTICA  
**Story Points:** 13  
**Labels:** Backend, Segurança, Autenticação  
**Status:** ⚠️ EM ANDAMENTO (Sistema básico OK, JWT pendente)

---

#### US005 - Validação e Sanitização de Inputs ✅

**Como** desenvolvedor  
**Eu quero** validar e sanitizar todos os inputs da aplicação  
**Para que** a aplicação esteja protegida contra ataques de injeção

**Critérios de Aceitação:**

- [x] Validação de dados no backend (Pydantic)
- [x] Sanitização contra SQL injection (SQLAlchemy ORM)
- [x] Validação no frontend implementada
- [x] Mensagens de erro padronizadas
- [x] Validação específica para dados de usuário

**Prioridade:** ⚠️ ALTA  
**Story Points:** 5  
**Labels:** Backend, Frontend, Segurança  
**Status:** ✅ CONCLUÍDO

---

#### US006 - Deploy da API na Nuvem

**Como** desenvolvedor  
**Eu quero** hospedar a API em uma plataforma cloud  
**Para que** a aplicação seja acessível publicamente de forma segura

**Critérios de Aceitação:**

- [ ] Plataforma cloud escolhida e configurada
- [ ] Variáveis de ambiente seguras configuradas
- [ ] Deploy do backend com HTTPS funcionando
- [ ] Domínio personalizado configurado
- [ ] Testes de conectividade e segurança realizados

**Prioridade:** 🔥 CRÍTICA  
**Story Points:** 8  
**Labels:** Backend, Deploy, Infraestrutura

---

#### US007 - Backup Seguro do MySQL

**Como** administrador  
**Eu quero** ter backups automáticos e seguros do MySQL  
**Para que** os dados sejam protegidos contra perda

**Critérios de Aceitação:**

- [ ] Backup automático do MySQL configurado na nuvem
- [ ] Criptografia de backups implementada
- [ ] Controle de acesso aos backups configurado
- [ ] Validação de integridade dos backups
- [ ] Logs de acesso aos dados implementados

**Prioridade:** 🔥 CRÍTICA  
**Story Points:** 5  
**Labels:** Backend, Segurança, Database

---

## 🏃‍♂️ SPRINT 2 - Segurança Avançada e Containerização

### 🎯 Objetivo do Sprint

Implementar criptografia de ponta a ponta, autenticação de 2 fatores e automatizar processos de desenvolvimento.

### 📋 User Stories

#### US007.1 - Criptografia de Ponta a Ponta

**Como** usuário  
**Eu quero** que meus dados sejam criptografados de ponta a ponta  
**Para que** minhas informações estejam protegidas durante toda a transmissão

**Critérios de Aceitação:**

- [ ] Criptografia end-to-end implementada no frontend
- [ ] Chaves de criptografia geradas no cliente
- [ ] Dados criptografados antes do envio para API
- [ ] Descriptografia segura no backend
- [ ] Rotação automática de chaves implementada
- [ ] Zero-knowledge para dados sensíveis

**Prioridade:** 🔥 CRÍTICA  
**Story Points:** 13  
**Labels:** Frontend, Backend, Segurança

---

#### US007.2 - Autenticação de 2 Fatores (2FA)

**Como** usuário  
**Eu quero** ter autenticação de 2 fatores ativada  
**Para que** minha conta tenha proteção adicional contra acessos não autorizados

**Critérios de Aceitação:**

- [ ] Integração com Google Authenticator/TOTP
- [ ] Códigos QR para configuração inicial
- [ ] Backup codes para recuperação
- [ ] SMS como método alternativo (opcional)
- [ ] Interface para ativar/desativar 2FA
- [ ] Validação obrigatória em login

**Prioridade:** 🔥 CRÍTICA  
**Story Points:** 13  
**Labels:** Frontend, Backend, Segurança

---

#### US008 - Containerização da Aplicação Flutter

**Como** desenvolvedor  
**Eu quero** containerizar a aplicação Flutter  
**Para que** o deploy seja consistente e reproduzível

**Critérios de Aceitação:**

- [ ] Dockerfile para Flutter Web criado
- [ ] Build otimizado para produção
- [ ] Nginx configurado para servir arquivos
- [ ] Container testado localmente
- [ ] Documentação de uso do container

**Prioridade:** ⚠️ ALTA  
**Story Points:** 8  
**Labels:** Frontend, Docker, Deploy

---

#### US009 - Orquestração com Docker Compose

**Como** desenvolvedor  
**Eu quero** orquestrar MySQL e aplicação com Docker Compose  
**Para que** toda a aplicação funcione de forma integrada e local

**Critérios de Aceitação:**

- [ ] docker-compose.yml criado com MySQL
- [ ] Rede entre containers configurada
- [ ] Volumes para persistência do banco
- [ ] Volume para modelos ML (.pkl)
- [ ] Variáveis de ambiente seguras configuradas
- [ ] Scripts de inicialização do banco

**Prioridade:** ⚠️ ALTA  
**Story Points:** 8  
**Labels:** DevOps, Docker, Database

---

#### US010 - Pipeline CI/CD Backend

**Como** desenvolvedor  
**Eu quero** ter deploy automático do backend  
**Para que** mudanças sejam aplicadas rapidamente e com segurança

**Critérios de Aceitação:**

- [ ] Workflow de build e test configurado
- [ ] Deploy automático para produção funcionando
- [ ] Testes automatizados integrados
- [ ] Notificações de status implementadas
- [ ] Rollback automático em caso de falha

**Prioridade:** ⚠️ ALTA  
**Story Points:** 8  
**Labels:** Backend, CI/CD, DevOps

---

#### US011 - Pipeline CI/CD Frontend

**Como** desenvolvedor  
**Eu quero** ter deploy automático do frontend Flutter  
**Para que** atualizações da interface sejam aplicadas automaticamente

**Critérios de Aceitação:**

- [ ] Build automático do Flutter configurado
- [ ] Deploy da versão web funcionando
- [ ] Testes de widget integrados
- [ ] Versionamento automático implementado
- [ ] Cache de dependências otimizado

**Prioridade:** ⚠️ ALTA  
**Story Points:** 8  
**Labels:** Frontend, CI/CD, DevOps

---

#### US012 - Testes Automatizados Backend

**Como** desenvolvedor  
**Eu quero** ter cobertura completa de testes para backend e banco  
**Para que** a qualidade e confiabilidade sejam garantidas

**Critérios de Aceitação:**

- [ ] Testes unitários dos serviços implementados
- [ ] Testes de integração da API funcionando
- [ ] Testes dos modelos ML implementados
- [ ] Testes de autenticação e autorização (MySQL)
- [ ] Testes de criptografia (MySQL)
- [ ] Coverage report configurado

**Prioridade:** 📝 MÉDIA  
**Story Points:** 13  
**Labels:** Backend, Testes, Qualidade, Database

---

## 🏃‍♂️ SPRINT 3 - Segurança Avançada e Finalização

### 🎯 Objetivo do Sprint

Implementar segurança avançada, monitoramento e finalizar a aplicação para entrega.

### 📋 User Stories

#### US013 - Segurança Avançada da API

**Como** desenvolvedor  
**Eu quero** implementar proteções adicionais na API  
**Para que** a aplicação seja resistente a ataques avançados

**Critérios de Aceitação:**

- [ ] Headers de segurança (CORS, CSP, HSTS) configurados
- [ ] Proteção contra ataques XSS implementada
- [ ] Validação rigorosa de dados funcionando
- [ ] Firewall básico configurado
- [ ] Testes de segurança realizados

**Prioridade:** ⚠️ ALTA  
**Story Points:** 8  
**Labels:** Backend, Segurança, API

---

#### US014 - Rate Limiting e Monitoramento de Segurança

**Como** administrador  
**Eu quero** monitorar e limitar atividades suspeitas  
**Para que** a aplicação seja protegida contra ataques e abusos

**Critérios de Aceitação:**

- [ ] Rate limiting na API por usuário implementado
- [ ] Logs de segurança estruturados funcionando
- [ ] Monitoramento de tentativas de login ativo
- [ ] Logs de ações dos usuários implementados
- [ ] Alertas automáticos de segurança configurados
- [ ] Detecção de atividades suspeitas funcionando

**Prioridade:** ⚠️ ALTA  
**Story Points:** 8  
**Labels:** Backend, Segurança, Monitoramento

---

#### US015 - Sistema de Logs Completo

**Como** desenvolvedor  
**Eu quero** ter um sistema robusto de logging  
**Para que** problemas possam ser diagnosticados rapidamente

**Critérios de Aceitação:**

- [ ] Logs estruturados (JSON) implementados
- [ ] Níveis de log (INFO, ERROR, DEBUG) configurados
- [ ] Rotação de logs funcionando
- [ ] Dashboard de monitoramento criado
- [ ] Alertas baseados em logs configurados

**Prioridade:** 📝 MÉDIA  
**Story Points:** 5  
**Labels:** Backend, Monitoramento, DevOps

---

#### US016 - Documentação Técnica ML

**Como** usuário técnico  
**Eu quero** documentação completa dos modelos ML  
**Para que** possa entender e manter os algoritmos

**Critérios de Aceitação:**

- [ ] Documentação dos modelos ML completa
- [ ] Métricas de performance documentadas
- [ ] Guia de retreinamento criado
- [ ] Explicação dos algoritmos implementada
- [ ] Exemplos de uso documentados

**Prioridade:** 📝 MÉDIA  
**Story Points:** 5  
**Labels:** ML, Documentação

---

#### US017 - Testes Finais e Otimização

**Como** desenvolvedor  
**Eu quero** realizar testes finais e otimizar a aplicação  
**Para que** a aplicação esteja pronta para produção

**Critérios de Aceitação:**

- [ ] Testes end-to-end completos realizados
- [ ] Otimização de performance implementada
- [ ] Verificação de todos os requisitos concluída
- [ ] Documentação de deploy finalizada
- [ ] Checklist de entrega completo

**Prioridade:** 🔥 CRÍTICA  
**Story Points:** 8  
**Labels:** Testes, Performance, Documentação

---

## 📊 Resumo dos Sprints

### Sprint 1 - Fundação Segura (Total: 60 Story Points)

- **Foco:** Segurança crítica e deploy básico
- **Cards Críticos:** 7 cards (60% críticos)
- **Principais Entregas:** HTTPS, PostgreSQL, Autenticação, Criptografia, Deploy

### Sprint 2 - Segurança Avançada e Automação (Total: 71 Story Points)

- **Foco:** Criptografia E2E, 2FA, Containerização e CI/CD
- **Cards Críticos:** 2 cards de segurança + 5 cards de automação
- **Principais Entregas:** Criptografia E2E, 2FA, Docker, CI/CD, Testes Automatizados

### Sprint 3 - Excelência (Total: 34 Story Points)

- **Foco:** Segurança avançada e finalização
- **Cards Finais:** 5 cards (40% críticos)
- **Principais Entregas:** Segurança Avançada, Logs, Documentação, Testes Finais

---

## 🏷️ Sistema de Labels

### Por Área:

- 🔴 **Backend** - Desenvolvimento da API
- 🔵 **Frontend** - Desenvolvimento Flutter
- 🟡 **DevOps** - Infraestrutura e deploy
- 🟢 **ML** - Machine Learning
- 🟣 **Database** - Banco de dados

### Por Prioridade:

- 🔥 **CRÍTICA** - Obrigatório para aprovação
- ⚠️ **ALTA** - Importante para qualidade
- 📝 **MÉDIA** - Desejável

### Por Tipo:

- 🔒 **Segurança** - Aspectos de segurança
- 🚀 **Deploy** - Publicação e infraestrutura
- 🧪 **Testes** - Qualidade e validação
- 📚 **Documentação** - Docs e manuais

---

## 🎯 Definition of Done

Para cada User Story ser considerada "Done":

- [ ] Código implementado e testado
- [ ] Pull request aprovado
- [ ] Deploy realizado (se aplicável)
- [ ] Documentação atualizada
- [ ] Testes passando
- [ ] Review de segurança (stories críticas)
- [ ] Critérios de aceitação validados

---

## 📊 Checklist de Entrega Final

### Para ser considerado COMPLETO:

- [ ] **ML modelo funcionando em produção**
- [ ] **API hospedada em nuvem com HTTPS**
- [ ] **App mobile funcionando**
- [ ] **Dados protegidos com criptografia**
- [ ] **Pipeline CI/CD ativo**
- [ ] **Containerização completa**

### Mínimo para APROVAÇÃO:

- [x] ✅ Modelo ML desenvolvido e treinado
- [x] ✅ API REST funcional com CRUD completo
- [x] ✅ App mobile multiplataforma
- [x] ✅ **MySQL para dados** (OBRIGATÓRIO)
- [x] ✅ **Sistema de usuários e autenticação básico** (OBRIGATÓRIO)
- [x] ✅ **Criptografia de senhas bcrypt** (OBRIGATÓRIO)
- [x] ✅ **Sistema completo: Usuários, Solicitações, Orçamentos, Avaliações**
- [ ] ❌ **Deploy em nuvem com HTTPS** (OBRIGATÓRIO)
- [ ] ⚠️ **JWT tokens** (ALTA PRIORIDADE)
- [ ] ❌ **Docker completo** (OBRIGATÓRIO)
