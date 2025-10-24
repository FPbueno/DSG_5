#!/bin/bash

# Script para executar a automação de issues do GitHub
# Projeto ABP WorcaFlow

echo "🚀 Iniciando automação de issues do GitHub..."
echo "=============================================="

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado. Instale o Python3 primeiro."
    exit 1
fi

# Verificar se o token do GitHub está configurado
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ GITHUB_TOKEN não configurado!"
    echo "Configure o token com: export GITHUB_TOKEN='seu_token_aqui'"
    exit 1
fi

# Verificar se o arquivo de script existe
if [ ! -f "create_github_issues.py" ]; then
    echo "❌ Arquivo create_github_issues.py não encontrado!"
    exit 1
fi

# Instalar dependências se necessário
echo "📦 Verificando dependências..."
pip3 install requests --quiet

# Executar o script
echo "🔧 Executando script de automação..."
python3 create_github_issues.py

echo "✅ Automação concluída!"
echo "📝 Verifique as issues criadas no GitHub"

