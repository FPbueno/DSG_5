# 📋 CARDS TRELLO - Projeto ABP WorcaFlow

## NOVO MODELO: Marketplace com Cliente e Prestador

## Organização em 3 Sprints

---

## 🏃‍♂️ **SPRINT 1 - Novo Modelo de Negócio**

_Foco: Implementar sistema de dois perfis e fluxo de orçamentos_

### 👥 **GESTÃO DE PERFIS**

**Card 1: Modelo de Usuários (Cliente e Prestador)**

- **Descrição:** Adaptar MySQL para dois tipos de perfil
- **Tarefas:**
  - [ ] Migrar schema MySQL para novo modelo
  - [ ] Tabela de Clientes (nome, email, cpf, endereço)
  - [ ] Tabela de Prestadores (categorias, regiões)
  - [ ] Sistema de autenticação por tipo de perfil
  - [ ] Validação de CPF/CNPJ
  - [ ] Criptografia de dados sensíveis
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, Database, Segurança

**Card 2: Sistema de Solicitações de Orçamento**

- **Descrição:** Cliente solicita orçamentos
- **Tarefas:**
  - [ ] Tabela de Solicitações no MySQL
  - [ ] Endpoint POST /solicitacoes/criar
  - [ ] Endpoint GET /solicitacoes/minhas
  - [ ] Estados da solicitação (aguardando/com orçamentos/fechada)
  - [ ] Validação de dados da solicitação
  - [ ] Tela Flutter: Criar Solicitação
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, Frontend, Database

**Card 3: ML com Limites de Preço**

- **Descrição:** ML calcula mínimo, sugerido e máximo
- **Tarefas:**
  - [ ] Adaptar modelo ML para calcular 3 valores
  - [ ] Endpoint POST /ml/calcular-limites-preco
  - [ ] Lógica: mínimo = sugerido × 0.7, máximo = sugerido × 1.5
  - [ ] Retornar limites junto com predição
  - [ ] Documentar algoritmo de limites
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, ML

**Card 4: Sistema de Orçamentos (Prestador)**

- **Descrição:** Prestador envia orçamento com limites
- **Tarefas:**
  - [ ] Tabela de Orçamentos no MySQL
  - [ ] Endpoint GET /solicitacoes/disponiveis (filtro por área)
  - [ ] Endpoint POST /orcamentos/criar
  - [ ] Validação: valor >= mínimo e <= máximo
  - [ ] Relacionar orçamento com solicitação
  - [ ] Tela Flutter: Criar Orçamento com limites visíveis
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, Frontend, Database

**Card 5: Comparação e Seleção de Orçamentos (Cliente)**

- **Descrição:** Cliente compara e escolhe orçamento
- **Tarefas:**
  - [ ] Endpoint GET /solicitacoes/{id}/orcamentos
  - [ ] Endpoint PUT /solicitacoes/{id}/aceitar-orcamento
  - [ ] Atualizar status dos orçamentos (aceito/recusado)
  - [ ] Notificar prestador selecionado
  - [ ] Tela Flutter: Comparar Orçamentos
  - [ ] Tela Flutter: Detalhes do Prestador
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, Frontend

**Card 3.1: Validação e Sanitização de Inputs**

- **Descrição:** Proteger contra ataques de injeção
- **Tarefas:**
  - [ ] Validação de dados no backend (Pydantic)
  - [ ] Sanitização de inputs SQL injection
  - [ ] Validação no frontend
  - [ ] Mensagens de erro padronizadas
  - [ ] Validação de dados de usuário
- **Prioridade:** ⚠️ ALTA
- **Labels:** Backend, Frontend, Segurança

### ☁️ **DEPLOY EM NUVEM**

**Card 4: Deploy da API na Nuvem**

- **Descrição:** Hospedar API em plataforma cloud
- **Tarefas:**
  - [ ] Escolher plataforma (Heroku/Railway/Render)
  - [ ] Configurar variáveis de ambiente seguras
  - [ ] Deploy do backend com HTTPS
  - [ ] Configurar domínio personalizado
  - [ ] Testes de conectividade e segurança
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, Deploy, Infraestrutura

**Card 5: Backup Seguro do PostgreSQL**

- **Descrição:** Backup seguro para PostgreSQL (usuários)
- **Tarefas:**
  - [ ] Backup automático do PostgreSQL (usuários) na nuvem
  - [ ] Criptografia de backups do PostgreSQL
  - [ ] Controle de acesso aos backups
  - [ ] Validação de integridade dos backups
  - [ ] Logs de acesso aos dados
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, Segurança, Database

---

## 🏃‍♂️ **SPRINT 2 - Segurança Avançada e Containerização**

_Foco: Treinar ML, Criptografia E2E, 2FA, Testes e Containerização_

### 🤖 **TREINAR MACHINE LEARNING**

**Card 5.1: Retreinamento e Otimização dos Modelos ML**

- **Descrição:** Melhorar e otimizar os modelos de Machine Learning
- **Tarefas:**
  - [ ] Análise de performance dos modelos atuais
  - [ ] Coleta de novos dados para treinamento
  - [ ] Retreinamento dos modelos com dados atualizados
  - [ ] Validação cruzada e métricas de performance
  - [ ] Otimização de hiperparâmetros
  - [ ] Testes A/B dos novos modelos
  - [ ] Documentação das melhorias implementadas
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** ML, Backend, Qualidade

### 🔐 **CRIPTOGRAFIA DE PONTA A PONTA**

**Card 5.2: Implementação de Criptografia E2E**

- **Descrição:** Implementar criptografia end-to-end para proteção máxima
- **Tarefas:**
  - [ ] Criptografia end-to-end no frontend Flutter
  - [ ] Chaves de criptografia geradas no cliente
  - [ ] Dados criptografados antes do envio para API
  - [ ] Descriptografia segura no backend
  - [ ] Rotação automática de chaves
  - [ ] Zero-knowledge para dados sensíveis
  - [ ] Testes de segurança da criptografia
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Frontend, Backend, Segurança

### 🔑 **CRIAÇÃO DE 2FA**

**Card 5.3: Autenticação de 2 Fatores (2FA)**

- **Descrição:** Implementar 2FA para proteção adicional das contas
- **Tarefas:**
  - [ ] Integração com Google Authenticator/TOTP
  - [ ] Códigos QR para configuração inicial
  - [ ] Backup codes para recuperação
  - [ ] SMS como método alternativo (opcional)
  - [ ] Interface Flutter para ativar/desativar 2FA
  - [ ] Validação obrigatória em login
  - [ ] Testes de segurança do 2FA
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Frontend, Backend, Segurança

### 🧪 **TESTES AUTOMATIZADOS**

**Card 5.4: Suite Completa de Testes**

- **Descrição:** Implementar testes abrangentes para toda a aplicação
- **Tarefas:**
  - [ ] Testes unitários dos serviços ML
  - [ ] Testes de integração da API
  - [ ] Testes de segurança (criptografia e 2FA)
  - [ ] Testes de autenticação e autorização
  - [ ] Testes de performance dos modelos ML
  - [ ] Coverage report configurado
  - [ ] Testes automatizados no CI/CD
- **Prioridade:** ⚠️ ALTA
- **Labels:** Backend, Frontend, Testes, Qualidade

### 🐳 **CONTAINERIZAÇÃO COMPLETA**

**Card 6: Dockerfile para Flutter**

- **Descrição:** Containerizar aplicação Flutter
- **Tarefas:**
  - [ ] Criar Dockerfile para Flutter Web
  - [ ] Otimizar build para produção
  - [ ] Configurar nginx para servir arquivos
  - [ ] Testar container localmente
- **Prioridade:** ⚠️ ALTA
- **Labels:** Frontend, Docker, Deploy

**Card 7: Docker Compose com PostgreSQL**

- **Descrição:** Orquestrar PostgreSQL (usuários) + Excel (dados ML)
- **Tarefas:**
  - [ ] Criar docker-compose.yml com PostgreSQL
  - [ ] Configurar rede entre containers
  - [ ] Volumes para persistência do banco de usuários
  - [ ] Volume para arquivo Excel (dados ML)
  - [ ] Variáveis de ambiente seguras
  - [ ] Scripts de inicialização do banco
- **Prioridade:** ⚠️ ALTA
- **Labels:** DevOps, Docker, Database

### 🔄 **CI/CD PIPELINE**

**Card 8: GitHub Actions - Backend**

- **Descrição:** Pipeline de CI/CD para API
- **Tarefas:**
  - [ ] Workflow de build e test
  - [ ] Deploy automático para produção
  - [ ] Testes automatizados
  - [ ] Notificações de status
- **Prioridade:** ⚠️ ALTA
- **Labels:** Backend, CI/CD, DevOps

**Card 9: GitHub Actions - Frontend**

- **Descrição:** Pipeline de CI/CD para Flutter
- **Tarefas:**
  - [ ] Build automático do Flutter
  - [ ] Deploy da versão web
  - [ ] Testes de widget
  - [ ] Versionamento automático
- **Prioridade:** ⚠️ ALTA
- **Labels:** Frontend, CI/CD, DevOps

### 🧪 **TESTES AUTOMATIZADOS**

**Card 10: Testes Backend e PostgreSQL**

- **Descrição:** Implementar testes da API, banco de usuários e dados ML
- **Tarefas:**
  - [ ] Testes unitários dos serviços
  - [ ] Testes de integração da API
  - [ ] Testes dos modelos ML (Excel)
  - [ ] Testes de autenticação e autorização (PostgreSQL)
  - [ ] Testes de criptografia (PostgreSQL)
  - [ ] Coverage report
- **Prioridade:** 📝 MÉDIA
- **Labels:** Backend, Testes, Qualidade, Database

---

## 🏃‍♂️ **SPRINT 3 - Segurança Avançada e Finalização**

_Foco: Completar requisitos e polimento final_

### 🔒 **SEGURANÇA AVANÇADA**

**Card 11: Segurança Avançada da API**

- **Descrição:** Implementar proteções adicionais
- **Tarefas:**
  - [ ] Headers de segurança (CORS, CSP, HSTS)
  - [ ] Proteção contra ataques XSS
  - [ ] Validação rigorosa de dados
  - [ ] Configurar firewall básico
- **Prioridade:** ⚠️ ALTA
- **Labels:** Backend, Segurança, API

**Card 12: Rate Limiting e Logs de Segurança**

- **Descrição:** Proteção contra ataques e monitoramento avançado
- **Tarefas:**
  - [ ] Rate limiting na API por usuário
  - [ ] Logs de segurança estruturados
  - [ ] Monitoramento de tentativas de login
  - [ ] Logs de ações dos usuários
  - [ ] Alertas automáticos de segurança
  - [ ] Detecção de atividades suspeitas
- **Prioridade:** ⚠️ ALTA
- **Labels:** Backend, Segurança, Monitoramento

### 📊 **MONITORAMENTO E LOGS**

**Card 13: Sistema de Logs**

- **Descrição:** Implementar logging completo
- **Tarefas:**
  - [ ] Logs estruturados (JSON)
  - [ ] Níveis de log (INFO, ERROR, DEBUG)
  - [ ] Rotação de logs
  - [ ] Dashboard de monitoramento
- **Prioridade:** 📝 MÉDIA
- **Labels:** Backend, Monitoramento, DevOps

### 🎯 **FINALIZAÇÃO E DOCUMENTAÇÃO**

**Card 14: Documentação Técnica ML**

- **Descrição:** Documentar modelos e algoritmos
- **Tarefas:**
  - [ ] Documentação dos modelos ML
  - [ ] Métricas de performance
  - [ ] Guia de retreinamento
  - [ ] Explicação dos algoritmos
- **Prioridade:** 📝 MÉDIA
- **Labels:** ML, Documentação

**Card 15: Testes Finais e Otimização**

- **Descrição:** Preparação para entrega
- **Tarefas:**
  - [ ] Testes end-to-end completos
  - [ ] Otimização de performance
  - [ ] Verificação de todos os requisitos
  - [ ] Documentação de deploy
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Testes, Performance, Documentação

---

## 📊 **RESUMO DOS SPRINTS**

### **SPRINT 1 - Fundação Segura Híbrida** ✅ **CONCLUÍDA**

- 🎯 **Objetivo:** Aplicação segura com PostgreSQL (usuários) + Excel (dados ML)
- 📈 **Entregáveis:** API com HTTPS + PostgreSQL (usuários) + Excel (ML) + Autenticação + Criptografia de Usuários
- 🔥 **Cards Críticos:** 1, 2, 2.1, 3, 4, 5

#### **📦 ENTREGAS DA SPRINT 1:**

- ✅ **API com HTTPS/TLS** configurado e funcionando
- ✅ **PostgreSQL** configurado para usuários
- ✅ **Sistema de autenticação JWT** implementado
- ✅ **Criptografia de usuários** (senhas e dados sensíveis)
- ✅ **Validação e sanitização** de inputs
- ✅ **Deploy da API** em nuvem
- ✅ **Backup seguro** do PostgreSQL
- ✅ **Documentação** de segurança implementada

### **SPRINT 2 - Segurança Avançada e Automação**

- 🎯 **Objetivo:** Treinar ML, Criptografia E2E, 2FA, Testes e Containerização
- 📈 **Entregáveis:** ML Otimizado + Criptografia E2E + 2FA + Testes + Docker + CI/CD
- 🔥 **Cards Críticos:** 5.1 (ML), 5.2 (Criptografia), 5.3 (2FA)
- ⚠️ **Cards Importantes:** 5.4 (Testes), 6, 7, 8, 9

#### **📦 ENTREGAS DA SPRINT 2:**

- [ ] **🤖 Modelos ML Retreinados** e otimizados
- [ ] **🔐 Criptografia de Ponta a Ponta** implementada
- [ ] **🔑 Autenticação de 2 Fatores (2FA)** funcionando
- [ ] **🧪 Suite Completa de Testes** implementada
- [ ] **🐳 Dockerfile para Flutter** criado e testado
- [ ] **🐳 Docker Compose** com PostgreSQL configurado
- [ ] **🔄 Pipeline CI/CD Backend** funcionando
- [ ] **🔄 Pipeline CI/CD Frontend** funcionando
- [ ] **📊 Deploy automático** configurado
- [ ] **📚 Documentação** de deploy e CI/CD

### **SPRINT 3 - Excelência**

- 🎯 **Objetivo:** Segurança total + Qualidade
- 📈 **Entregáveis:** Criptografia + Logs + Docs
- 🏆 **Cards Finais:** 11, 12, 15

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

## 🏷️ **LABELS SUGERIDAS PARA TRELLO**

### **Por Área:**

- 🔴 **Backend** - Desenvolvimento da API
- 🔵 **Frontend** - Desenvolvimento Flutter
- 🟡 **DevOps** - Infraestrutura e deploy
- 🟢 **ML** - Machine Learning
- 🟣 **Database** - Banco de dados

### **Por Prioridade:**

- 🔥 **CRÍTICA** - Obrigatório para aprovação
- ⚠️ **ALTA** - Importante para qualidade
- 📝 **MÉDIA** - Desejável

### **Por Tipo:**

- 🔒 **Segurança** - Aspectos de segurança
- 🚀 **Deploy** - Publicação e infraestrutura
- 🧪 **Testes** - Qualidade e validação
- 📚 **Documentação** - Docs e manuais

---

## ⏱️ **CRONOGRAMA SUGERIDO**

- **Semana 1:** Sprint 1 (Seg-Sex)
- **Semana 2:** Sprint 2 (Seg-Qui)
- **Semana 2:** Sprint 3 (Sex-Dom)

---

## 📊 **CHECKLIST DE ENTREGA FINAL**

### **Para considerado COMPLETO:**

- [ ] **ML modelo funcionando em produção**
- [ ] **API hospedada em nuvem com HTTPS**
- [ ] **App mobile funcionando**
- [ ] **Dados protegidos com criptografia**
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

---

## 🎯 **DEFINITION OF DONE**

Para cada card ser considerado "Done":

- [ ] Código implementado e testado
- [ ] Pull request aprovado
- [ ] Deploy realizado (se aplicável)
- [ ] Documentação atualizada
- [ ] Testes passando
- [ ] Review de segurança (cards críticos)
