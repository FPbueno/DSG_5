# 📋 CARDS TRELLO - Projeto ABP WorcaFlow

## 🏃‍♂️ **SPRINT 1 - FUNDAÇÃO SEGURA**

**📅 DATAS:** 22/09 - 24/09, 26/09, 30/09, 02/10

### 👥 **GESTÃO DE PERFIS**

**Card S1-001: Modelo de Usuários (Cliente e Prestador)** ✅ **CONCLUÍDO**

- **Descrição:** Adaptar MySQL para dois tipos de perfil
- **Tarefas:**
  - [x] Migrar schema MySQL para novo modelo
  - [x] Tabela de Clientes (nome, email, cpf, endereço)
  - [x] Tabela de Prestadores (categorias, regiões)
  - [x] Sistema de autenticação por tipo de perfil
  - [x] Validação de CPF/CNPJ
  - [x] Criptografia de dados sensíveis
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, Database, Segurança
- **Data:** 22/09/2025

**Card S1-002: Sistema de Solicitações de Orçamento** ✅ **CONCLUÍDO**

- **Descrição:** Cliente solicita orçamentos
- **Tarefas:**
  - [x] Tabela de Solicitações no MySQL
  - [x] Endpoint POST /solicitacoes/criar
  - [x] Endpoint GET /solicitacoes/minhas
  - [x] Estados da solicitação (aguardando/com orçamentos/fechada)
  - [x] Validação de dados da solicitação
  - [x] Tela Flutter: Criar Solicitação
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, Frontend, Database
- **Data:** 24/09/2025

**Card S1-003: ML com Limites de Preço** ✅ **CONCLUÍDO**

- **Descrição:** ML calcula mínimo, sugerido e máximo
- **Tarefas:**
  - [x] Adaptar modelo ML para calcular 3 valores
  - [x] Endpoint POST /ml/calcular-limites-preco
  - [x] Lógica: mínimo = sugerido × 0.7, máximo = sugerido × 1.5
  - [x] Retornar limites junto com predição
  - [x] Documentar algoritmo de limites
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, ML
- **Data:** 24/09/2025

**Card S1-004: Sistema de Orçamentos (Prestador)** ✅ **CONCLUÍDO**

- **Descrição:** Prestador envia orçamento com limites
- **Tarefas:**
  - [x] Tabela de Orçamentos no MySQL
  - [x] Endpoint GET /solicitacoes/disponiveis (filtro por área)
  - [x] Endpoint POST /orcamentos/criar
  - [x] Validação: valor >= mínimo e <= máximo
  - [x] Relacionar orçamento com solicitação
  - [x] Tela Flutter: Criar Orçamento com limites visíveis
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, Frontend, Database
- **Data:** 26/09/2025

**Card S1-005: Comparação e Seleção de Orçamentos (Cliente)** ✅ **CONCLUÍDO**

- **Descrição:** Cliente compara e escolhe orçamento
- **Tarefas:**
  - [x] Endpoint GET /solicitacoes/{id}/orcamentos
  - [x] Endpoint PUT /solicitacoes/{id}/aceitar-orcamento
  - [x] Atualizar status dos orçamentos (aceito/recusado)
  - [x] Notificar prestador selecionado
  - [x] Tela Flutter: Comparar Orçamentos
  - [x] Tela Flutter: Detalhes do Prestador
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** Backend, Frontend
- **Data:** 30/09/2025

**Card S1-006: Validação e Sanitização de Inputs** ✅ **CONCLUÍDO**

- **Descrição:** Proteger contra ataques de injeção
- **Tarefas:**
  - [x] Validação de dados no backend (Pydantic)
  - [x] Sanitização de inputs SQL injection
  - [x] Validação no frontend
  - [x] Mensagens de erro padronizadas
  - [x] Validação de dados de usuário
- **Prioridade:** ⚠️ ALTA
- **Labels:** Backend, Frontend, Segurança
- **Data:** 02/10/2025

---

## 🏃‍♂️ **SPRINT 2 - SEGURANÇA AVANÇADA E AUTOMAÇÃO**

**📅 DATAS:** 13/10 - 15/10, 17/10, 21/10, 22/10, 23/10

### 🤖 **AM - APRENDIZAGEM DE MÁQUINA**

**Card AM-001: Análise e Diagnóstico dos Modelos Atuais**

- **Descrição:** Avaliar performance e identificar pontos de melhoria
- **Tarefas:**
  - [ ] Análise de métricas atuais (precisão, recall, F1-score)
  - [ ] Identificação de gaps nos dados de treinamento
  - [ ] Análise de viés nos modelos existentes
  - [ ] Documentação dos problemas identificados
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** AM, Backend, Qualidade
- **Data:** 13/10/2025

**Card AM-002: Coleta e Preparação de Dados**

- **Descrição:** Coletar e preparar novos dados para retreinamento
- **Tarefas:**
  - [ ] Coleta de dados históricos adicionais
  - [ ] Limpeza e normalização dos dados
  - [ ] Feature engineering e seleção de variáveis
  - [ ] Divisão em conjuntos de treino/validação/teste
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** AM, Backend, Qualidade
- **Data:** 15/10/2025

**Card AM-003: Retreinamento e Otimização**

- **Descrição:** Retreinar modelos com dados atualizados
- **Tarefas:**
  - [ ] Retreinamento do modelo de categorias
  - [ ] Retreinamento do modelo de preços
  - [ ] Otimização de hiperparâmetros
  - [ ] Validação cruzada e métricas de performance
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** AM, Backend, Qualidade
- **Data:** 17/10/2025

**Card AM-004: Testes e Validação dos Modelos**

- **Descrição:** Validar novos modelos antes do deploy
- **Tarefas:**
  - [ ] Testes A/B dos novos modelos
  - [ ] Comparação de performance (antes vs depois)
  - [ ] Testes de robustez e edge cases
  - [ ] Documentação das melhorias implementadas
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** AM, Backend, Qualidade
- **Data:** 21/10/2025

**Card AM-005: Testes de Machine Learning**

- **Descrição:** Implementar testes específicos para modelos ML
- **Tarefas:**
  - [ ] Testes unitários dos serviços ML
  - [ ] Testes de performance dos modelos
  - [ ] Testes de precisão e recall
  - [ ] Testes de integração com a API
- **Prioridade:** ⚠️ ALTA
- **Labels:** AM, Backend, Testes, Qualidade
- **Data:** 22/10/2025

### 🔐 **SD - SEGURANÇA DE DADOS**

**Card SD-001: Implementação de Criptografia E2E Frontend** ✅ **CONCLUÍDO**

- **Descrição:** Implementar criptografia no lado do cliente
- **Tarefas:**
  - [x] Implementar biblioteca de criptografia no Flutter (encrypt package)
  - [x] Gerar chaves de criptografia no cliente (busca chave pública do backend)
  - [x] Criptografar dados sensíveis antes do envio (senha criptografada no login)
  - [ ] Implementar rotação automática de chaves
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** SD, Frontend, Segurança
- **Data:** 21/10/2025

**Card SD-002: Implementação de Criptografia E2E Backend** ✅ **CONCLUÍDO**

- **Descrição:** Implementar descriptografia segura no servidor
- **Tarefas:**
  - [x] Implementar descriptografia no backend (decrypt_rsa_password)
  - [x] Gerenciamento seguro de chaves no servidor (chaves RSA geradas no startup)
  - [ ] Implementar zero-knowledge para dados sensíveis
  - [ ] Logs de auditoria para operações de criptografia
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** SD, Backend, Segurança
- **Data:** 21/10/2025

**Card SD-003: Autenticação de 2 Fatores (2FA)**

- **Descrição:** Implementar 2FA para proteção adicional
- **Tarefas:**
  - [ ] Integração com Google Authenticator/TOTP
  - [ ] Geração de códigos QR para configuração
  - [ ] Implementar backup codes para recuperação
  - [ ] Interface Flutter para ativar/desativar 2FA
  - [ ] Validação obrigatória em login
- **Prioridade:** 🔥 CRÍTICA
- **Labels:** SD, Frontend, Backend, Segurança
- **Data:** 21/10/2025

**Card SD-004: Testes de Segurança** ✅ **PARCIALMENTE CONCLUÍDO**

- **Descrição:** Implementar testes abrangentes de segurança
- **Tarefas:**
  - [x] Testes de penetração da criptografia E2E (test_security_rsa.py, test_rsa_endpoints.py)
  - [ ] Testes de segurança do sistema 2FA
  - [ ] Testes de vulnerabilidades comuns (OWASP)
  - [ ] Auditoria de segurança dos dados
- **Prioridade:** ⚠️ ALTA
- **Labels:** SD, Backend, Frontend, Testes, Segurança
- **Data:** 22/10/2025

**Card SD-005: Testes de Segurança e Autenticação** ✅ **PARCIALMENTE CONCLUÍDO**

- **Descrição:** Implementar testes de segurança abrangentes
- **Tarefas:**
  - [ ] Testes de autenticação e autorização
  - [x] Testes de integração da API (endpoint /public-key e /login com RSA)
  - [x] Testes de criptografia e 2FA (testes RSA implementados)
  - [ ] Coverage report configurado
- **Prioridade:** ⚠️ ALTA
- **Labels:** SD, Backend, Frontend, Testes, Qualidade
- **Data:** 22/10/2025

### ☁️ **CN - COMPUTAÇÃO EM NUVEM**

**Card CN-001: Containerização da Aplicação Flutter**

- **Descrição:** Containerizar aplicação Flutter para deploy em nuvem
- **Tarefas:**
  - [ ] Criar Dockerfile para Flutter Web
  - [ ] Otimizar build para produção
  - [ ] Configurar nginx para servir arquivos
  - [ ] Testar container localmente
  - [ ] Configurar variáveis de ambiente
- **Prioridade:** ⚠️ ALTA
- **Labels:** CN, Frontend, Docker, Deploy
- **Data:** 22/10/2025

**Card CN-002: Orquestração com Docker Compose**

- **Descrição:** Orquestrar PostgreSQL + Excel (dados ML) em containers
- **Tarefas:**
  - [ ] Criar docker-compose.yml com PostgreSQL
  - [ ] Configurar rede entre containers
  - [ ] Volumes para persistência do banco de usuários
  - [ ] Volume para arquivo Excel (dados ML)
  - [ ] Variáveis de ambiente seguras
  - [ ] Scripts de inicialização do banco
- **Prioridade:** ⚠️ ALTA
- **Labels:** CN, DevOps, Docker, Database
- **Data:** 22/10/2025

**Card CN-003: Pipeline CI/CD Backend**

- **Descrição:** Implementar pipeline de CI/CD para API
- **Tarefas:**
  - [ ] Configurar workflow de build e test
  - [ ] Implementar deploy automático para produção
  - [ ] Integrar testes automatizados no pipeline
  - [ ] Configurar notificações de status
  - [ ] Implementar rollback automático em caso de falha
- **Prioridade:** ⚠️ ALTA
- **Labels:** CN, Backend, CI/CD, DevOps
- **Data:** 22/10/2025

**Card CN-004: Pipeline CI/CD Frontend**

- **Descrição:** Implementar pipeline de CI/CD para Flutter
- **Tarefas:**
  - [ ] Configurar build automático do Flutter
  - [ ] Implementar deploy da versão web
  - [ ] Integrar testes de widget
  - [ ] Configurar versionamento automático
  - [ ] Otimizar cache de dependências
- **Prioridade:** ⚠️ ALTA
- **Labels:** CN, Frontend, CI/CD, DevOps
- **Data:** 22/10/2025

### 📱 **PD - PROGRAMAÇÃO DISPOSITIVOS MÓVEIS**

**Card PD-001: Otimização da Interface Mobile**

- **Descrição:** Melhorar experiência do usuário em dispositivos móveis
- **Tarefas:**
  - [ ] Otimizar layouts para diferentes tamanhos de tela
  - [ ] Implementar gestos touch nativos
  - [ ] Melhorar performance em dispositivos móveis
  - [ ] Implementar cache offline para dados essenciais
- **Prioridade:** ⚠️ ALTA
- **Labels:** PD, Frontend, Mobile, UX
- **Data:** 22/10/2025

**Card PD-002: Integração com Recursos Mobile**

- **Descrição:** Aproveitar recursos específicos de dispositivos móveis
- **Tarefas:**
  - [ ] Implementar notificações push
  - [ ] Integrar com câmera para upload de imagens
  - [ ] Implementar geolocalização para prestadores
  - [ ] Configurar biometria para autenticação
- **Prioridade:** ⚠️ ALTA
- **Labels:** PD, Frontend, Mobile, Segurança
- **Data:** 23/10/2025

**Card PD-003: Testes em Dispositivos Móveis**

- **Descrição:** Implementar testes específicos para mobile
- **Tarefas:**
  - [ ] Testes de widget em diferentes dispositivos
  - [ ] Testes de performance mobile
  - [ ] Testes de usabilidade em dispositivos reais
  - [ ] Testes de compatibilidade com diferentes versões
- **Prioridade:** ⚠️ ALTA
- **Labels:** PD, Frontend, Mobile, Testes, Qualidade
- **Data:** 23/10/2025

---

## 🏃‍♂️ **SPRINT 3 - SEGURANÇA AVANÇADA E FINALIZAÇÃO**

**📅 DATAS:** 6/11 - 10/11, 12/11, 14/11, 18/11

### 🔒 **SEGURANÇA AVANÇADA**

**Card S3-011: Segurança Avançada da API**

- **Descrição:** Implementar proteções adicionais
- **Tarefas:**
  - [ ] Headers de segurança (CORS, CSP, HSTS)
  - [ ] Proteção contra ataques XSS
  - [ ] Validação rigorosa de dados
  - [ ] Configurar firewall básico
- **Prioridade:** ⚠️ ALTA
- **Labels:** Backend, Segurança, API
- **Data:** 6/11/2025

**Card S3-012: Rate Limiting e Logs de Segurança**

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

**Card S3-013: Sistema de Logs**

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

**Card S3-014: Documentação Técnica ML**

- **Descrição:** Documentar modelos e algoritmos
- **Tarefas:**
  - [ ] Documentação dos modelos ML
  - [ ] Métricas de performance
  - [ ] Guia de retreinamento
  - [ ] Explicação dos algoritmos
- **Prioridade:** 📝 MÉDIA
- **Labels:** ML, Documentação
- **Data:** 14/11/2025

**Card S3-015: Testes Finais e Otimização**

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

### **SPRINT 1 - Fundação Segura** ✅ **CONCLUÍDA**

- 🎯 **Objetivo:** Sistema de dois perfis e fluxo de orçamentos
- 🔥 **Cards Críticos:** S1-001 ✅, S1-002 ✅, S1-003 ✅, S1-004 ✅, S1-005 ✅, S1-006 ✅

### **SPRINT 2 - Segurança Avançada e Automação**

- 🎯 **Objetivo:** AM (ML) + SD (Segurança) + CN (Nuvem) + PD (Mobile)
- 🔥 **Cards Críticos:** AM-001 a AM-004, SD-001 a SD-003
- ⚠️ **Cards Importantes:** CN-001 a CN-004, PD-001 a PD-003, AM-005, SD-004, SD-005

### **SPRINT 3 - Segurança Avançada e Finalização**

- 🎯 **Objetivo:** Segurança total + Qualidade
- 🏆 **Cards Finais:** S3-011, S3-012, S3-015

---

## 🏷️ **LABELS POR PRIORIDADE**

- 🔥 **CRÍTICA** - Obrigatório para aprovação
- ⚠️ **ALTA** - Importante para qualidade
- 📝 **MÉDIA** - Desejável
