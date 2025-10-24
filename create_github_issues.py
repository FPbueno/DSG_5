#!/usr/bin/env python3
"""
Script para automatizar criação de issues no GitHub
Baseado no cronograma das Sprints 1 e 2 do projeto ABP
"""

import requests
import json
from datetime import datetime
import os

# Tentar importar configurações do arquivo config.py
try:
    from config import GITHUB_TOKEN, REPO_OWNER, REPO_NAME
    print("✅ Configurações carregadas do arquivo config.py")
except ImportError:
    # Configurações padrão
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    REPO_OWNER = 'seu-usuario'  # Substitua pelo seu usuário/organização
    REPO_NAME = 'ABP'  # Substitua pelo nome do repositório
    print("⚠️ Usando configurações padrão. Configure config.py ou variáveis de ambiente.")
    print("💡 Dica: Copie config_example.py para config.py e configure seus dados")

# Headers para API do GitHub
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
    'Content-Type': 'application/json'
}

def create_issue(title, body, labels, assignees=None, milestone=None):
    """Cria uma issue no GitHub"""
    url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues'
    
    data = {
        'title': title,
        'body': body,
        'labels': labels
    }
    
    if assignees:
        data['assignees'] = assignees
    
    if milestone:
        data['milestone'] = milestone
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 201:
        print(f"✅ Issue criada: {title}")
        return response.json()
    else:
        print(f"❌ Erro ao criar issue '{title}': {response.status_code}")
        print(f"Resposta: {response.text}")
        return None

def sprint_1_issues():
    """Cria issues da Sprint 1"""
    print("🚀 Criando issues da Sprint 1...")
    
    # Sprint 1 - Issues
    issues_sprint1 = [
        {
            'title': 'SD-001: Configurar HTTPS/TLS',
            'body': '''## 🔒 Configuração HTTPS/TLS

**Descrição:** Implementar comunicação segura HTTPS/TLS para a aplicação

**Critérios de Aceitação:**
- [ ] Certificado SSL configurado para API
- [ ] HTTPS habilitado no servidor
- [ ] URLs do Flutter atualizadas para HTTPS
- [ ] Comunicação segura testada e funcionando
- [ ] Redirecionamento HTTP → HTTPS implementado

**Prioridade:** 🔥 CRÍTICA
**Responsável:** Isaac, Renan
**Data:** 22/09/2025''',
            'labels': ['SD', 'Backend', 'Segurança', 'crítica'],
            'assignees': ['Isaac', 'Renan']
        },
        {
            'title': 'LD-001: Desenvolver logotipo representativo',
            'body': '''## 🎨 Desenvolvimento de Logotipo

**Descrição:** Criar um logotipo representativo e original para o projeto WorcaFlow

**Critérios de Aceitação:**
- [ ] Logotipo criado e aprovado pela equipe
- [ ] Versões em diferentes formatos (PNG, SVG)
- [ ] Integração no aplicativo Flutter
- [ ] Documentação do processo de criação

**Prioridade:** ⚠️ ALTA
**Responsável:** Felipe, Marcelly, Ana
**Data:** 22/09/2025''',
            'labels': ['LD', 'Frontend', 'Design', 'alta'],
            'assignees': ['Felipe', 'Marcelly', 'Ana']
        },
        {
            'title': 'CN-015: Configuração do Banco de Dados',
            'body': '''## 🗄️ Configuração do Banco de Dados

**Descrição:** Configurar MySQL para dados de usuários e transações

**Critérios de Aceitação:**
- [ ] MySQL configurado para a aplicação
- [ ] Schema de usuários e autenticação criado
- [ ] Sistema de roles e permissões implementado
- [ ] Modelos ML mantidos separados (arquivos .pkl)
- [ ] Backup automático do banco configurado

**Prioridade:** 🔥 CRÍTICA
**Responsável:** Isaac, Renan
**Data:** 24/09/2025''',
            'labels': ['CN', 'Backend', 'Database', 'crítica'],
            'assignees': ['Isaac', 'Renan']
        },
        {
            'title': 'AM-003: Criação de dados sintéticos para treinamento',
            'body': '''## 🤖 Criação de Dados Sintéticos

**Descrição:** Gerar dados sintéticos para treinamento do modelo de ML

**Critérios de Aceitação:**
- [ ] Dados sintéticos gerados com qualidade
- [ ] Validação dos dados sintéticos
- [ ] Integração com pipeline de treinamento
- [ ] Documentação do processo de geração

**Prioridade:** ⚠️ ALTA
**Responsável:** Felipe, Marcelly
**Data:** 24/09/2025, 26/09/2025, 30/09/2025, 02/10/2025''',
            'labels': ['AM', 'ML', 'Dados', 'alta'],
            'assignees': ['Felipe', 'Marcelly']
        },
        {
            'title': 'AM-004: Teste do modelo de machine learning',
            'body': '''## 🧪 Teste do Modelo ML

**Descrição:** Testar e validar o modelo de machine learning

**Critérios de Aceitação:**
- [ ] Testes de precisão e recall
- [ ] Validação cruzada implementada
- [ ] Métricas de performance documentadas
- [ ] Testes de integração com API

**Prioridade:** ⚠️ ALTA
**Responsável:** Marcelly
**Data:** 24/09/2025, 30/09/2025''',
            'labels': ['AM', 'ML', 'Testes', 'alta'],
            'assignees': ['Marcelly']
        },
        {
            'title': 'LD-003: Desenvolvimento Front-end',
            'body': '''## 📱 Desenvolvimento Front-end

**Descrição:** Desenvolver interface do usuário em Flutter

**Critérios de Aceitação:**
- [ ] Telas principais implementadas
- [ ] Navegação entre telas funcionando
- [ ] Integração com API backend
- [ ] Testes de interface implementados

**Prioridade:** ⚠️ ALTA
**Responsável:** Ana
**Data:** 24/09/2025, 26/09/2025, 30/09/2025, 02/10/2025''',
            'labels': ['LD', 'Frontend', 'Flutter', 'alta'],
            'assignees': ['Ana']
        }
    ]
    
    for issue in issues_sprint1:
        create_issue(
            title=issue['title'],
            body=issue['body'],
            labels=issue['labels'],
            assignees=issue['assignees']
        )

def sprint_2_issues():
    """Cria issues da Sprint 2"""
    print("🚀 Criando issues da Sprint 2...")
    
    # Sprint 2 - Issues
    issues_sprint2 = [
        {
            'title': 'AM-001: Análise e Diagnóstico dos Modelos Atuais',
            'body': '''## 🤖 Análise e Diagnóstico dos Modelos ML

**Descrição:** Avaliar performance e identificar pontos de melhoria dos modelos atuais

**Critérios de Aceitação:**
- [ ] AM-001.1: Análise de métricas atuais (precisão, recall, F1-score)
- [ ] AM-001.2: Identificação de gaps nos dados de treinamento
- [ ] AM-001.3: Análise de viés nos modelos existentes
- [ ] AM-001.4: Documentação dos problemas identificados

**Prioridade:** 🔥 CRÍTICA
**Responsável:** Isaac
**Data:** 13/10/2025''',
            'labels': ['AM', 'ML', 'Análise', 'crítica'],
            'assignees': ['Isaac']
        },
        {
            'title': 'AM-002: Coleta e Preparação de Dados',
            'body': '''## 📊 Coleta e Preparação de Dados

**Descrição:** Coletar e preparar novos dados para retreinamento

**Critérios de Aceitação:**
- [ ] AM-002.1: Coleta de dados históricos adicionais
- [ ] AM-002.2: Limpeza e normalização dos dados
- [ ] AM-002.3: Feature engineering e seleção de variáveis
- [ ] AM-002.4: Divisão em conjuntos de treino/validação/teste

**Prioridade:** 🔥 CRÍTICA
**Responsável:** Felipe
**Data:** 15/10/2025''',
            'labels': ['AM', 'ML', 'Dados', 'crítica'],
            'assignees': ['Felipe']
        },
        {
            'title': 'AM-003: Retreinamento e Otimização',
            'body': '''## 🔄 Retreinamento e Otimização

**Descrição:** Retreinar modelos com dados atualizados

**Critérios de Aceitação:**
- [ ] AM-003.1: Retreinamento do modelo de categorias
- [ ] AM-003.2: Retreinamento do modelo de preços
- [ ] AM-003.3: Otimização de hiperparâmetros
- [ ] AM-003.4: Validação cruzada e métricas de performance

**Prioridade:** 🔥 CRÍTICA
**Responsável:** Marcelly
**Data:** 17/10/2025''',
            'labels': ['AM', 'ML', 'Treinamento', 'crítica'],
            'assignees': ['Marcelly']
        },
        {
            'title': 'SD-001: Criptografia E2E Frontend',
            'body': '''## 🔐 Criptografia E2E Frontend

**Descrição:** Implementar criptografia no lado do cliente

**Critérios de Aceitação:**
- [ ] SD-001.1: Implementar biblioteca de criptografia no Flutter
- [ ] SD-001.2: Gerar chaves de criptografia no cliente
- [ ] SD-001.3: Criptografar dados sensíveis antes do envio
- [ ] SD-001.4: Implementar rotação automática de chaves

**Prioridade:** 🔥 CRÍTICA
**Responsável:** Ana
**Data:** 21/10/2025''',
            'labels': ['SD', 'Frontend', 'Segurança', 'crítica'],
            'assignees': ['Ana']
        },
        {
            'title': 'SD-002: Criptografia E2E Backend',
            'body': '''## 🔐 Criptografia E2E Backend

**Descrição:** Implementar descriptografia segura no servidor

**Critérios de Aceitação:**
- [ ] SD-002.1: Implementar descriptografia no backend
- [ ] SD-002.2: Gerenciamento seguro de chaves no servidor
- [ ] SD-002.3: Implementar zero-knowledge para dados sensíveis
- [ ] SD-002.4: Logs de auditoria para operações de criptografia

**Prioridade:** 🔥 CRÍTICA
**Responsável:** Renan
**Data:** 21/10/2025''',
            'labels': ['SD', 'Backend', 'Segurança', 'crítica'],
            'assignees': ['Renan']
        },
        {
            'title': 'SD-003: Autenticação de 2 Fatores (2FA)',
            'body': '''## 🔑 Autenticação de 2 Fatores

**Descrição:** Implementar 2FA para proteção adicional

**Critérios de Aceitação:**
- [ ] SD-003.1: Integração com Google Authenticator/TOTP
- [ ] SD-003.2: Geração de códigos QR para configuração
- [ ] SD-003.3: Implementar backup codes para recuperação
- [ ] SD-003.4: Interface Flutter para ativar/desativar 2FA
- [ ] SD-003.5: Validação obrigatória em login

**Prioridade:** 🔥 CRÍTICA
**Responsável:** Isaac
**Data:** 21/10/2025''',
            'labels': ['SD', 'Frontend', 'Backend', 'Segurança', 'crítica'],
            'assignees': ['Isaac']
        },
        {
            'title': 'CN-001: Containerização da Aplicação Flutter',
            'body': '''## 🐳 Containerização Flutter

**Descrição:** Containerizar aplicação Flutter para deploy em nuvem

**Critérios de Aceitação:**
- [ ] CN-001.1: Criar Dockerfile para Flutter Web
- [ ] CN-001.2: Otimizar build para produção
- [ ] CN-001.3: Configurar nginx para servir arquivos
- [ ] CN-001.4: Testar container localmente
- [ ] CN-001.5: Configurar variáveis de ambiente

**Prioridade:** ⚠️ ALTA
**Responsável:** Ana
**Data:** 22/10/2025''',
            'labels': ['CN', 'Frontend', 'Docker', 'Deploy', 'alta'],
            'assignees': ['Ana']
        },
        {
            'title': 'CN-002: Orquestração com Docker Compose',
            'body': '''## 🐳 Docker Compose

**Descrição:** Orquestrar PostgreSQL + Excel (dados ML) em containers

**Critérios de Aceitação:**
- [ ] CN-002.1: Criar docker-compose.yml com PostgreSQL
- [ ] CN-002.2: Configurar rede entre containers
- [ ] CN-002.3: Volumes para persistência do banco de usuários
- [ ] CN-002.4: Volume para arquivo Excel (dados ML)
- [ ] CN-002.5: Variáveis de ambiente seguras
- [ ] CN-002.6: Scripts de inicialização do banco

**Prioridade:** ⚠️ ALTA
**Responsável:** Renan
**Data:** 22/10/2025''',
            'labels': ['CN', 'DevOps', 'Docker', 'Database', 'alta'],
            'assignees': ['Renan']
        },
        {
            'title': 'CN-003: Pipeline CI/CD Backend',
            'body': '''## 🔄 Pipeline CI/CD Backend

**Descrição:** Implementar pipeline de CI/CD para API

**Critérios de Aceitação:**
- [ ] CN-003.1: Configurar workflow de build e test
- [ ] CN-003.2: Implementar deploy automático para produção
- [ ] CN-003.3: Integrar testes automatizados no pipeline
- [ ] CN-003.4: Configurar notificações de status
- [ ] CN-003.5: Implementar rollback automático em caso de falha

**Prioridade:** ⚠️ ALTA
**Responsável:** Isaac
**Data:** 22/10/2025''',
            'labels': ['CN', 'Backend', 'CI/CD', 'DevOps', 'alta'],
            'assignees': ['Isaac']
        },
        {
            'title': 'CN-004: Pipeline CI/CD Frontend',
            'body': '''## 🔄 Pipeline CI/CD Frontend

**Descrição:** Implementar pipeline de CI/CD para Flutter

**Critérios de Aceitação:**
- [ ] CN-004.1: Configurar build automático do Flutter
- [ ] CN-004.2: Implementar deploy da versão web
- [ ] CN-004.3: Integrar testes de widget
- [ ] CN-004.4: Configurar versionamento automático
- [ ] CN-004.5: Otimizar cache de dependências

**Prioridade:** ⚠️ ALTA
**Responsável:** Felipe
**Data:** 22/10/2025''',
            'labels': ['CN', 'Frontend', 'CI/CD', 'DevOps', 'alta'],
            'assignees': ['Felipe']
        },
        {
            'title': 'PD-001: Otimização da Interface Mobile',
            'body': '''## 📱 Otimização Interface Mobile

**Descrição:** Melhorar experiência do usuário em dispositivos móveis

**Critérios de Aceitação:**
- [ ] PD-001.1: Otimizar layouts para diferentes tamanhos de tela
- [ ] PD-001.2: Implementar gestos touch nativos
- [ ] PD-001.3: Melhorar performance em dispositivos móveis
- [ ] PD-001.4: Implementar cache offline para dados essenciais

**Prioridade:** ⚠️ ALTA
**Responsável:** Marcelly
**Data:** 22/10/2025''',
            'labels': ['PD', 'Frontend', 'Mobile', 'UX', 'alta'],
            'assignees': ['Marcelly']
        },
        {
            'title': 'PD-002: Integração com Recursos Mobile',
            'body': '''## 📱 Recursos Mobile

**Descrição:** Aproveitar recursos específicos de dispositivos móveis

**Critérios de Aceitação:**
- [ ] PD-002.1: Implementar notificações push
- [ ] PD-002.2: Integrar com câmera para upload de imagens
- [ ] PD-002.3: Implementar geolocalização para prestadores
- [ ] PD-002.4: Configurar biometria para autenticação

**Prioridade:** ⚠️ ALTA
**Responsável:** Ana
**Data:** 23/10/2025''',
            'labels': ['PD', 'Frontend', 'Mobile', 'Segurança', 'alta'],
            'assignees': ['Ana']
        },
        {
            'title': 'PD-003: Testes em Dispositivos Móveis',
            'body': '''## 📱 Testes Mobile

**Descrição:** Implementar testes específicos para mobile

**Critérios de Aceitação:**
- [ ] PD-003.1: Testes de widget em diferentes dispositivos
- [ ] PD-003.2: Testes de performance mobile
- [ ] PD-003.3: Testes de usabilidade em dispositivos reais
- [ ] PD-003.4: Testes de compatibilidade com diferentes versões

**Prioridade:** ⚠️ ALTA
**Responsável:** Renan
**Data:** 23/10/2025''',
            'labels': ['PD', 'Frontend', 'Mobile', 'Testes', 'Qualidade', 'alta'],
            'assignees': ['Renan']
        }
    ]
    
    for issue in issues_sprint2:
        create_issue(
            title=issue['title'],
            body=issue['body'],
            labels=issue['labels'],
            assignees=issue['assignees']
        )

def main():
    """Função principal"""
    print("🚀 Iniciando criação automática de issues do GitHub...")
    print("=" * 60)
    
    if not GITHUB_TOKEN:
        print("❌ Erro: GITHUB_TOKEN não encontrado!")
        print("Configure a variável de ambiente GITHUB_TOKEN")
        return
    
    print(f"📁 Repositório: {REPO_OWNER}/{REPO_NAME}")
    print("=" * 60)
    
    # Criar issues da Sprint 1
    print("\n📋 SPRINT 1 - FUNDAÇÃO SEGURA")
    sprint_1_issues()
    
    print("\n" + "=" * 60)
    
    # Criar issues da Sprint 2
    print("\n📋 SPRINT 2 - SEGURANÇA AVANÇADA E AUTOMAÇÃO")
    sprint_2_issues()
    
    print("\n" + "=" * 60)
    print("✅ Processo concluído!")
    print("📝 Verifique as issues criadas no GitHub")

if __name__ == "__main__":
    main()
