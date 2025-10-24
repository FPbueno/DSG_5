#!/usr/bin/env python3
"""
Script para automatizar criação de issues no GitHub usando SSH
Baseado no cronograma das Sprints 1 e 2 do projeto ABP
"""

import subprocess
import json
import os

# Configurações do GitHub
REPO_OWNER = 'seu-usuario'  # Substitua pelo seu usuário
REPO_NAME = 'ABP'  # Substitua pelo nome do repositório

def create_issue_ssh(title, body, labels, assignees=None):
    """Cria uma issue no GitHub usando SSH"""
    
    # Preparar dados da issue
    issue_data = {
        'title': title,
        'body': body,
        'labels': labels
    }
    
    if assignees:
        issue_data['assignees'] = assignees
    
    # Criar comando gh CLI
    cmd = ['gh', 'issue', 'create']
    cmd.extend(['--title', title])
    cmd.extend(['--body', body])
    
    for label in labels:
        cmd.extend(['--label', label])
    
    if assignees:
        for assignee in assignees:
            cmd.extend(['--assignee', assignee])
    
    try:
        # Executar comando
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ Issue criada: {title}")
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar issue '{title}': {e}")
        print(f"Erro: {e.stderr}")
        return None

def main():
    """Função principal"""
    print("🚀 Iniciando criação automática de issues do GitHub via SSH...")
    print("=" * 60)
    
    # Verificar se gh CLI está instalado
    try:
        subprocess.run(['gh', '--version'], capture_output=True, check=True)
        print("✅ GitHub CLI encontrado")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ GitHub CLI não encontrado!")
        print("Instale: https://cli.github.com/")
        return
    
    # Verificar autenticação SSH
    try:
        subprocess.run(['gh', 'auth', 'status'], capture_output=True, check=True)
        print("✅ Autenticação SSH configurada")
    except subprocess.CalledProcessError:
        print("❌ Não autenticado!")
        print("Execute: gh auth login")
        return
    
    print(f"📁 Repositório: {REPO_OWNER}/{REPO_NAME}")
    print("=" * 60)
    
    # Criar issues da Sprint 1
    print("\n📋 SPRINT 1 - FUNDAÇÃO SEGURA")
    
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
        }
    ]
    
    for issue in issues_sprint1:
        create_issue_ssh(
            title=issue['title'],
            body=issue['body'],
            labels=issue['labels'],
            assignees=issue['assignees']
        )
    
    print("\n✅ Processo concluído!")
    print("📝 Verifique as issues criadas no GitHub")

if __name__ == "__main__":
    main()
