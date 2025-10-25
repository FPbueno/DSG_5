# 📋 CARDS TRELLO - Projeto ABP WorcaFlow

## NOVO MODELO: Marketplace com Cliente e Prestador

## Organização em 3 Sprints

---

## 🏃‍♂️ **SPRINT 1 - FUNDAÇÃO SEGURA**

**📅 DATAS:** 22/09 - 24/09, 26/09, 30/09, 02/10

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
- **Data:** 22/09/2025

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
- **Data:** 24/09/2025

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
- **Data:** 24/09/2025

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
- **Data:** 26/09/2025

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
- **Data:** 30/09/2025

**Card 6: Validação e Sanitização de Inputs**

- **Descrição:** Proteger contra ataques de injeção
- **Tarefas:**
  - [ ] Validação de dados no backend (Pydantic)
  - [ ] Sanitização de inputs SQL injection
  - [ ] Validação no frontend
  - [ ] Mensagens de erro padronizadas
  - [ ] Validação de dados de usuário
- **Prioridade:** ⚠️ ALTA
- **Labels:** Backend, Frontend, Segurança
- **Data:** 02/10/2025

---

## 🏃‍♂️ **SPRINT 2 - SEGURANÇA AVANÇADA E AUTOMAÇÃO**

**📅 DATAS:** 13/10 - 15/10, 17/10, 21/10, 22/10, 23/10

_Foco: Treinar ML, Criptografia E2E, 2FA, Testes e Containerização_

### 🤖 **AM - APRENDIZAGEM DE MÁQUINA**

**Card AM-001: Análise e Diagnóstico dos Modelos Atuais**

- **Descrição:** Avaliar performance e identificar pontos de melhoria
- **Tarefas:**
  - [ ] AM-001.1: Análise de métricas atuais (precisão, recall, F1-score)
  - [ ] AM-001.2: Identificação de gaps nos dados de treinamento
  - [ ] AM-001.3: Análise de viés nos modelos existentes
  - [ ] AM-001.4: Documentação dos problemas identificados
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** AM, Backend, Qualidade
- **Data:** 13/10/2025

**Card AM-002: Coleta e Preparação de Dados**

- **Descrição:** Coletar e preparar novos dados para retreinamento
- **Tarefas:**
  - [ ] AM-002.1: Coleta de dados históricos adicionais
  - [ ] AM-002.2: Limpeza e normalização dos dados
  - [ ] AM-002.3: Feature engineering e seleção de variáveis
  - [ ] AM-002.4: Divisão em conjuntos de treino/validação/teste
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** AM, Backend, Qualidade
- **Data:** 15/10/2025

**Card AM-003: Retreinamento e Otimização**

- **Descrição:** Retreinar modelos com dados atualizados
- **Tarefas:**
  - [ ] AM-003.1: Retreinamento do modelo de categorias
  - [ ] AM-003.2: Retreinamento do modelo de preços
  - [ ] AM-003.3: Otimização de hiperparâmetros
  - [ ] AM-003.4: Validação cruzada e métricas de performance
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** AM, Backend, Qualidade
- **Data:** 17/10/2025

**Card AM-004: Testes e Validação dos Modelos**

- **Descrição:** Validar novos modelos antes do deploy
- **Tarefas:**
  - [ ] AM-004.1: Testes A/B dos novos modelos
  - [ ] AM-004.2: Comparação de performance (antes vs depois)
  - [ ] AM-004.3: Testes de robustez e edge cases
  - [ ] AM-004.4: Documentação das melhorias implementadas
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** AM, Backend, Qualidade
- **Data:** 21/10/2025

### 🔐 **SD - SEGURANÇA DE DADOS**

**Card SD-001: Implementação de Criptografia E2E Frontend**

- **Descrição:** Implementar criptografia no lado do cliente
- **Tarefas:**
  - [ ] SD-001.1: Implementar biblioteca de criptografia no Flutter
  - [ ] SD-001.2: Gerar chaves de criptografia no cliente
  - [ ] SD-001.3: Criptografar dados sensíveis antes do envio
  - [ ] SD-001.4: Implementar rotação automática de chaves
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** SD, Frontend, Segurança
- **Data:** 21/10/2025

**Card SD-002: Implementação de Criptografia E2E Backend**

- **Descrição:** Implementar descriptografia segura no servidor
- **Tarefas:**
  - [ ] SD-002.1: Implementar descriptografia no backend
  - [ ] SD-002.2: Gerenciamento seguro de chaves no servidor
  - [ ] SD-002.3: Implementar zero-knowledge para dados sensíveis
  - [ ] SD-002.4: Logs de auditoria para operações de criptografia
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** SD, Backend, Segurança
- **Data:** 21/10/2025

**Card SD-003: Autenticação de 2 Fatores (2FA)**

- **Descrição:** Implementar 2FA para proteção adicional
- **Tarefas:**
  - [ ] SD-003.1: Integração com Google Authenticator/TOTP
  - [ ] SD-003.2: Geração de códigos QR para configuração
  - [ ] SD-003.3: Implementar backup codes para recuperação
  - [ ] SD-003.4: Interface Flutter para ativar/desativar 2FA
  - [ ] SD-003.5: Validação obrigatória em login
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** SD, Frontend, Backend, Segurança
- **Data:** 21/10/2025

**Card SD-004: Testes de Segurança**

- **Descrição:** Implementar testes abrangentes de segurança
- **Tarefas:**
  - [ ] SD-004.1: Testes de penetração da criptografia E2E
  - [ ] SD-004.2: Testes de segurança do sistema 2FA
  - [ ] SD-004.3: Testes de vulnerabilidades comuns (OWASP)
  - [ ] SD-004.4: Auditoria de segurança dos dados
- **Prioridade:** ⚠️ ALTA
- **Labels:** SD, Backend, Frontend, Testes, Segurança
- **Data:** 22/10/2025

### 🧪 **TESTES AUTOMATIZADOS**

**Card AM-005: Testes de Machine Learning**

- **Descrição:** Implementar testes específicos para modelos ML
- **Tarefas:**
  - [ ] AM-005.1: Testes unitários dos serviços ML
  - [ ] AM-005.2: Testes de performance dos modelos
  - [ ] AM-005.3: Testes de precisão e recall
  - [ ] AM-005.4: Testes de integração com a API
- **Prioridade:** ⚠️ ALTA
- **Labels:** AM, Backend, Testes, Qualidade
- **Data:** 22/10/2025

**Card SD-005: Testes de Segurança e Autenticação**

- **Descrição:** Implementar testes de segurança abrangentes
- **Tarefas:**
  - [ ] SD-005.1: Testes de autenticação e autorização
  - [ ] SD-005.2: Testes de integração da API
  - [ ] SD-005.3: Testes de criptografia e 2FA
  - [ ] SD-005.4: Coverage report configurado
- **Prioridade:** ⚠️ ALTA
- **Labels:** SD, Backend, Frontend, Testes, Qualidade
- **Data:** 22/10/2025

### ☁️ **CN - COMPUTAÇÃO EM NUVEM**

**Card CN-001: Containerização da Aplicação Flutter**

- **Descrição:** Containerizar aplicação Flutter para deploy em nuvem
- **Tarefas:**
  - [ ] CN-001.1: Criar Dockerfile para Flutter Web
  - [ ] CN-001.2: Otimizar build para produção
  - [ ] CN-001.3: Configurar nginx para servir arquivos
  - [ ] CN-001.4: Testar container localmente
  - [ ] CN-001.5: Configurar variáveis de ambiente
- **Prioridade:** ⚠️ ALTA
- **Labels:** CN, Frontend, Docker, Deploy
- **Data:** 22/10/2025

**Card CN-002: Orquestração com Docker Compose**

- **Descrição:** Orquestrar PostgreSQL + Excel (dados ML) em containers
- **Tarefas:**
  - [ ] CN-002.1: Criar docker-compose.yml com PostgreSQL
  - [ ] CN-002.2: Configurar rede entre containers
  - [ ] CN-002.3: Volumes para persistência do banco de usuários
  - [ ] CN-002.4: Volume para arquivo Excel (dados ML)
  - [ ] CN-002.5: Variáveis de ambiente seguras
  - [ ] CN-002.6: Scripts de inicialização do banco
- **Prioridade:** ⚠️ ALTA
- **Labels:** CN, DevOps, Docker, Database
- **Data:** 22/10/2025

**Card CN-003: Pipeline CI/CD Backend**

- **Descrição:** Implementar pipeline de CI/CD para API
- **Tarefas:**
  - [ ] CN-003.1: Configurar workflow de build e test
  - [ ] CN-003.2: Implementar deploy automático para produção
  - [ ] CN-003.3: Integrar testes automatizados no pipeline
  - [ ] CN-003.4: Configurar notificações de status
  - [ ] CN-003.5: Implementar rollback automático em caso de falha
- **Prioridade:** ⚠️ ALTA
- **Labels:** CN, Backend, CI/CD, DevOps
- **Data:** 22/10/2025

**Card CN-004: Pipeline CI/CD Frontend**

- **Descrição:** Implementar pipeline de CI/CD para Flutter
- **Tarefas:**
  - [ ] CN-004.1: Configurar build automático do Flutter
  - [ ] CN-004.2: Implementar deploy da versão web
  - [ ] CN-004.3: Integrar testes de widget
  - [ ] CN-004.4: Configurar versionamento automático
  - [ ] CN-004.5: Otimizar cache de dependências
- **Prioridade:** ⚠️ ALTA
- **Labels:** CN, Frontend, CI/CD, DevOps
- **Data:** 22/10/2025

### 📱 **PD - PROGRAMAÇÃO DISPOSITIVOS MÓVEIS**

**Card PD-001: Otimização da Interface Mobile**

- **Descrição:** Melhorar experiência do usuário em dispositivos móveis
- **Tarefas:**
  - [ ] PD-001.1: Otimizar layouts para diferentes tamanhos de tela
  - [ ] PD-001.2: Implementar gestos touch nativos
  - [ ] PD-001.3: Melhorar performance em dispositivos móveis
  - [ ] PD-001.4: Implementar cache offline para dados essenciais
- **Prioridade:** ⚠️ ALTA
- **Labels:** PD, Frontend, Mobile, UX
- **Data:** 22/10/2025

**Card PD-002: Integração com Recursos Mobile**

- **Descrição:** Aproveitar recursos específicos de dispositivos móveis
- **Tarefas:**
  - [ ] PD-002.1: Implementar notificações push
  - [ ] PD-002.2: Integrar com câmera para upload de imagens
  - [ ] PD-002.3: Implementar geolocalização para prestadores
  - [ ] PD-002.4: Configurar biometria para autenticação
- **Prioridade:** ⚠️ ALTA
- **Labels:** PD, Frontend, Mobile, Segurança
- **Data:** 23/10/2025

**Card PD-003: Testes em Dispositivos Móveis**

- **Descrição:** Implementar testes específicos para mobile
- **Tarefas:**
  - [ ] PD-003.1: Testes de widget em diferentes dispositivos
  - [ ] PD-003.2: Testes de performance mobile
  - [ ] PD-003.3: Testes de usabilidade em dispositivos reais
  - [ ] PD-003.4: Testes de compatibilidade com diferentes versões
- **Prioridade:** ⚠️ ALTA
- **Labels:** PD, Frontend, Mobile, Testes, Qualidade
- **Data:** 23/10/2025

---

## 🏃‍♂️ **SPRINT 3 - SEGURANÇA AVANÇADA E FINALIZAÇÃO**

**📅 DATAS:** 6/11 - 10/11, 12/11, 14/11, 18/11

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
- **Data:** 6/11/2025

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
- **Data:** 10/11/2025

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
- **Data:** 12/11/2025

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
- **Data:** 14/11/2025

**Card 15: Testes Finais e Otimização**

- **Descrição:** Preparação para entrega
- **Tarefas:**
  - [ ] Testes end-to-end completos
  - [ ] Otimização de performance
  - [ ] Verificação de todos os requisitos
  - [ ] Documentação de deploy
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Testes, Performance, Documentação
- **Data:** 18/11/2025

---

## 📊 **RESUMO DOS SPRINTS**

### **SPRINT 1 - Fundação Segura Híbrida** ✅ **CONCLUÍDA**

- 🎯 **Objetivo:** Aplicação segura com MySQL (usuários) + Excel (dados ML)
- 📈 **Entregáveis:** API com HTTPS + MySQL (usuários) + Excel (ML) + Autenticação + Criptografia de Usuários
- 🔥 **Cards Críticos:** 1, 2, 2.1, 3, 4, 5

#### **📦 ENTREGAS DA SPRINT 1:**

- ✅ **API com HTTPS/TLS** configurado e funcionando
- ✅ **MySQL** configurado para usuários
- ✅ **Sistema de autenticação JWT** implementado
- ✅ **Criptografia de usuários** (senhas e dados sensíveis)
- ✅ **Validação e sanitização** de inputs
- ✅ **Deploy da API** em nuvem
- ✅ **Backup seguro** do MySQL
- ✅ **Documentação** de segurança implementada

### **SPRINT 2 - Segurança Avançada e Automação**

- 🎯 **Objetivo:** AM (ML) + SD (Segurança) + CN (Nuvem) + PD (Mobile)
- 📈 **Entregáveis:** ML Otimizado + Criptografia E2E + 2FA + Testes + Docker + CI/CD + Mobile
- 🔥 **Cards Críticos:** AM-001 a AM-004, SD-001 a SD-003
- ⚠️ **Cards Importantes:** CN-001 a CN-004, PD-001 a PD-003, AM-005, SD-004, SD-005

#### **📦 ENTREGAS DA SPRINT 2:**

**🤖 AM - APRENDIZAGEM DE MÁQUINA:**

- [ ] **AM-001:** Análise e diagnóstico dos modelos atuais
- [ ] **AM-002:** Coleta e preparação de dados
- [ ] **AM-003:** Retreinamento e otimização
- [ ] **AM-004:** Testes e validação dos modelos
- [ ] **AM-005:** Testes de Machine Learning

**🔐 SD - SEGURANÇA DE DADOS:**

- [ ] **SD-001:** Criptografia E2E Frontend
- [ ] **SD-002:** Criptografia E2E Backend
- [ ] **SD-003:** Autenticação de 2 Fatores (2FA)
- [ ] **SD-004:** Testes de segurança
- [ ] **SD-005:** Testes de segurança e autenticação

**☁️ CN - COMPUTAÇÃO EM NUVEM:**

- [ ] **CN-001:** Containerização da aplicação Flutter
- [ ] **CN-002:** Orquestração com Docker Compose
- [ ] **CN-003:** Pipeline CI/CD Backend
- [ ] **CN-004:** Pipeline CI/CD Frontend

**📱 PD - PROGRAMAÇÃO DISPOSITIVOS MÓVEIS:**

- [ ] **PD-001:** Otimização da interface mobile
- [ ] **PD-002:** Integração com recursos mobile
- [ ] **PD-003:** Testes em dispositivos móveis

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

### \*\*Por Prioridade:

- 🔥 **CRÍTICA** - Obrigatório para aprovação
- ⚠️ **ALTA** - Importante para qualidade
- 📝 **MÉDIA** - Desejável

### **Por Tipo:**

- 🔒 **Segurança** - Aspectos de segurança
- 🚀 **Deploy** - Publicação e infraestrutura
- 🧪 **Testes** - Qualidade e validação
- 📚 **Documentação** - Docs e manuais

---

## ⏱️ **CRONOGRAMA DETALHADO - OUTUBRO 2025**

### 📅 **SPRINT 2 - CRONOGRAMA DETALHADO**

#### **🗓️ OUTUBRO 10 (SEGUNDA-FEIRA) - INÍCIO SPRINT 2**

**👥 EQUIPE - TAREFAS DISTRIBUÍDAS**

**Isaac - 13/10/2025**

- **AM-001:** Análise e Diagnóstico dos Modelos Atuais
  - AM-001.1: Análise de métricas atuais (precisão, recall, F1-score)
  - AM-001.2: Identificação de gaps nos dados de treinamento
  - AM-001.3: Análise de viés nos modelos existentes
  - AM-001.4: Documentação dos problemas identificados

**Felipe - 15/10/2025**

- **AM-002:** Coleta e Preparação de Dados
  - AM-002.1: Coleta de dados históricos adicionais
  - AM-002.2: Limpeza e normalização dos dados
  - AM-002.3: Feature engineering e seleção de variáveis
  - AM-002.4: Divisão em conjuntos de treino/validação/teste

**Marcelly - 17/10/2025**

- **AM-003:** Retreinamento e Otimização
  - AM-003.1: Retreinamento do modelo de categorias
  - AM-003.2: Retreinamento do modelo de preços
  - AM-003.3: Otimização de hiperparâmetros
  - AM-003.4: Validação cruzada e métricas de performance

**Ana - 21/10/2025**

- **SD-001:** Implementação de Criptografia E2E Frontend
  - SD-001.1: Implementar biblioteca de criptografia no Flutter
  - SD-001.2: Gerar chaves de criptografia no cliente
  - SD-001.3: Criptografar dados sensíveis antes do envio
  - SD-001.4: Implementar rotação automática de chaves

**Renan - 21/10/2025**

- **SD-002:** Implementação de Criptografia E2E Backend
  - SD-002.1: Implementar descriptografia no backend
  - SD-002.2: Gerenciamento seguro de chaves no servidor
  - SD-002.3: Implementar zero-knowledge para dados sensíveis
  - SD-002.4: Logs de auditoria para operações de criptografia

---

#### **🗓️ OUTUBRO 15 (TERÇA-FEIRA) - MEIO DA SPRINT 2**

**👥 EQUIPE - CONTINUAÇÃO DAS TAREFAS**

**Isaac - 21/10/2025**

- **SD-003:** Autenticação de 2 Fatores (2FA)
  - SD-003.1: Integração com Google Authenticator/TOTP
  - SD-003.2: Geração de códigos QR para configuração
  - SD-003.3: Implementar backup codes para recuperação

**Felipe - 21/10/2025**

- **AM-004:** Testes e Validação dos Modelos
  - AM-004.1: Testes A/B dos novos modelos
  - AM-004.2: Comparação de performance (antes vs depois)
  - AM-004.3: Testes de robustez e edge cases
  - AM-004.4: Documentação das melhorias implementadas

**Marcelly - 21/10/2025**

- **AM-005:** Testes de Machine Learning
  - AM-005.1: Testes unitários dos serviços ML
  - AM-005.2: Testes de performance dos modelos
  - AM-005.3: Testes de precisão e recall
  - AM-005.4: Testes de integração com a API

**Ana - 22/10/2025**

- **CN-001:** Containerização da Aplicação Flutter
  - CN-001.1: Criar Dockerfile para Flutter Web
  - CN-001.2: Otimizar build para produção
  - CN-001.3: Configurar nginx para servir arquivos
  - CN-001.4: Testar container localmente
  - CN-001.5: Configurar variáveis de ambiente

**Renan - 22/10/2025**

- **CN-002:** Orquestração com Docker Compose
  - CN-002.1: Criar docker-compose.yml com PostgreSQL
  - CN-002.2: Configurar rede entre containers
  - CN-002.3: Volumes para persistência do banco de usuários
  - CN-002.4: Volume para arquivo Excel (dados ML)
  - CN-002.5: Variáveis de ambiente seguras
  - CN-002.6: Scripts de inicialização do banco

---

#### **🗓️ OUTUBRO 17 (QUINTA-FEIRA) - DESENVOLVIMENTO INTENSIVO**

**👥 EQUIPE - FINALIZAÇÃO E DEPLOY**

**Isaac - 22/10/2025**

- **CN-003:** Pipeline CI/CD Backend
  - CN-003.1: Configurar workflow de build e test
  - CN-003.2: Implementar deploy automático para produção
  - CN-003.3: Integrar testes automatizados no pipeline
  - CN-003.4: Configurar notificações de status
  - CN-003.5: Implementar rollback automático em caso de falha

**Felipe - 22/10/2025**

- **CN-004:** Pipeline CI/CD Frontend
  - CN-004.1: Configurar build automático do Flutter
  - CN-004.2: Implementar deploy da versão web
  - CN-004.3: Integrar testes de widget
  - CN-004.4: Configurar versionamento automático
  - CN-004.5: Otimizar cache de dependências

**Marcelly - 22/10/2025**

- **PD-001:** Otimização da Interface Mobile
  - PD-001.1: Otimizar layouts para diferentes tamanhos de tela
  - PD-001.2: Implementar gestos touch nativos
  - PD-001.3: Melhorar performance em dispositivos móveis
  - PD-001.4: Implementar cache offline para dados essenciais

**Ana - 23/10/2025**

- **PD-002:** Integração com Recursos Mobile
  - PD-002.1: Implementar notificações push
  - PD-002.2: Integrar com câmera para upload de imagens
  - PD-002.3: Implementar geolocalização para prestadores
  - PD-002.4: Configurar biometria para autenticação

**Renan - 23/10/2025**

- **PD-003:** Testes em Dispositivos Móveis
  - PD-003.1: Testes de widget em diferentes dispositivos
  - PD-003.2: Testes de performance mobile
  - PD-003.3: Testes de usabilidade em dispositivos reais
  - PD-003.4: Testes de compatibilidade com diferentes versões

---

### 📊 **RESUMO DO CRONOGRAMA**

- **Outubro 10:** Início - Análise ML + Criptografia Frontend
- **Outubro 15:** Desenvolvimento - Dados ML + Criptografia + Containerização
- **Outubro 17:** Intensivo - Retreinamento + 2FA + Docker + Mobile
- **Outubro 21:** Testes - Validação ML + Segurança + CI/CD + Mobile
- **Outubro 23:** Finalização - Deploy + Testes Finais + Mobile

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
