# 🤖 Automação de Issues GitHub - Projeto ABP

## 📋 Descrição

Script Python para automatizar a criação de issues no GitHub baseado no cronograma das Sprints 1 e 2 do projeto ABP WorcaFlow.

## 🚀 Como Usar

### 1. Configuração Inicial

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/ABP.git
cd ABP

# Instale as dependências
pip install requests

# Configure o token do GitHub
export GITHUB_TOKEN="seu_token_github_aqui"
```

### 2. Configurar o Script

Edite o arquivo `create_github_issues.py` e ajuste:

```python
REPO_OWNER = 'seu-usuario'  # Seu usuário/organização
REPO_NAME = 'ABP'  # Nome do repositório
```

### 3. Executar o Script

```bash
python create_github_issues.py
```

## 📊 Issues Criadas

### Sprint 1 - Fundação Segura

- **SD-001:** Configurar HTTPS/TLS (Isaac, Renan)
- **LD-001:** Desenvolver logotipo (Felipe, Marcelly, Ana)
- **CN-015:** Configuração do Banco de Dados (Isaac, Renan)
- **AM-003:** Criação de dados sintéticos (Felipe, Marcelly)
- **AM-004:** Teste do modelo ML (Marcelly)
- **LD-003:** Desenvolvimento Front-end (Ana)

### Sprint 2 - Segurança Avançada e Automação

- **AM-001:** Análise e Diagnóstico dos Modelos (Isaac)
- **AM-002:** Coleta e Preparação de Dados (Felipe)
- **AM-003:** Retreinamento e Otimização (Marcelly)
- **SD-001:** Criptografia E2E Frontend (Ana)
- **SD-002:** Criptografia E2E Backend (Renan)
- **SD-003:** Autenticação de 2 Fatores (Isaac)
- **CN-001:** Containerização Flutter (Ana)
- **CN-002:** Docker Compose (Renan)
- **CN-003:** Pipeline CI/CD Backend (Isaac)
- **CN-004:** Pipeline CI/CD Frontend (Felipe)
- **PD-001:** Otimização Interface Mobile (Marcelly)
- **PD-002:** Recursos Mobile (Ana)
- **PD-003:** Testes Mobile (Renan)

## 🏷️ Labels Utilizadas

### Por Área:

- **AM** - Aprendizagem de Máquina
- **SD** - Segurança de Dados
- **CN** - Computação em Nuvem
- **PD** - Programação Dispositivos Móveis
- **LD** - Liderança e Design

### Por Prioridade:

- **crítica** - Obrigatório para aprovação
- **alta** - Importante para qualidade

### Por Tipo:

- **Backend** - Desenvolvimento da API
- **Frontend** - Desenvolvimento Flutter
- **Segurança** - Aspectos de segurança
- **ML** - Machine Learning
- **Docker** - Containerização
- **CI/CD** - Automação
- **Mobile** - Dispositivos móveis
- **Testes** - Qualidade e validação

## 👥 Membros da Equipe

- **Isaac** - Análise ML, 2FA, CI/CD Backend
- **Felipe** - Dados ML, CI/CD Frontend
- **Marcelly** - Retreinamento ML, Interface Mobile
- **Ana** - Criptografia Frontend, Containerização, Recursos Mobile
- **Renan** - Criptografia Backend, Docker Compose, Testes Mobile

## 📅 Cronograma

### Sprint 1 (Setembro 2025)

- 16/09: Reuniões de alinhamento
- 18/09: Reuniões de alinhamento
- 22/09: HTTPS/TLS + Logotipo
- 24/09: Banco de dados + Dados sintéticos + Testes ML + Frontend
- 26/09: HTTPS/TLS + Dados sintéticos + Frontend
- 30/09: Configuração banco + Dados sintéticos + Testes ML + Frontend
- 02/10: Frontend + Dados sintéticos + Configuração banco

### Sprint 2 (Outubro 2025)

- 13/10: Análise ML (Isaac)
- 15/10: Dados ML (Felipe)
- 17/10: Retreinamento ML (Marcelly)
- 21/10: Criptografia E2E (Ana, Renan) + 2FA (Isaac) + Testes ML (Felipe, Marcelly)
- 22/10: Containerização (Ana, Renan) + CI/CD (Isaac, Felipe) + Mobile (Marcelly)
- 23/10: Recursos Mobile (Ana) + Testes Mobile (Renan)

## 🔧 Personalização

Para adicionar novas issues ou modificar as existentes, edite as funções:

- `sprint_1_issues()` - Issues da Sprint 1
- `sprint_2_issues()` - Issues da Sprint 2

## 📝 Notas Importantes

1. **Token GitHub:** Necessário ter permissões de escrita no repositório
2. **Labels:** Certifique-se de que as labels existem no repositório
3. **Assignees:** Verifique se os nomes dos usuários estão corretos
4. **Milestones:** Pode ser adicionado posteriormente para organizar por sprint

## 🚨 Troubleshooting

### Erro de Token

```
❌ Erro: GITHUB_TOKEN não encontrado!
```

**Solução:** Configure a variável de ambiente:

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
```

### Erro 404 - Repositório não encontrado

**Solução:** Verifique se `REPO_OWNER` e `REPO_NAME` estão corretos

### Erro 422 - Labels não existem

**Solução:** Crie as labels necessárias no GitHub ou remova labels inexistentes do script

## 📞 Suporte

Para dúvidas ou problemas, consulte:

- Documentação da API do GitHub: https://docs.github.com/en/rest
- Issues do repositório: https://github.com/seu-usuario/ABP/issues

