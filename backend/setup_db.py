#!/usr/bin/env python3
"""
Script para configurar e inicializar o banco de dados MySQL
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório do projeto ao path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from api.v1.core.database import create_tables, engine
from api.v1.models.user import User
from api.v1.models.db_models import Cliente, Prestador, Solicitacao, Orcamento

def main():
    """Função principal para configurar o banco de dados"""
    print("🔧 Configurando banco de dados MySQL...")
    
    try:
        # Testa a conexão com o banco
        print("📡 Testando conexão com o banco de dados...")
        connection = engine.connect()
        connection.close()
        print("✅ Conexão com o banco estabelecida com sucesso!")
        
        # Cria as tabelas
        print("📋 Criando tabelas...")
        create_tables()
        print("✅ Tabelas criadas com sucesso!")
        
        print("\n🎉 Banco de dados configurado com sucesso!")
        print("📊 Tabelas disponíveis:")
        print("   - users (usuários)")
        print("   - clientes (novos perfis de cliente)")
        print("   - prestadores (novos perfis de prestador)")
        print("   - solicitacoes (solicitações de orçamento)")
        print("   - orcamentos (orçamentos dos prestadores)")
        print("\n🚀 Você pode agora iniciar a API com: python main.py")
        
    except Exception as e:
        print(f"❌ Erro ao configurar o banco de dados: {e}")
        print("\n🔍 Verifique:")
        print("   1. Se as credenciais do banco estão corretas")
        print("   2. Se o servidor MySQL está acessível")
        print("   3. Se as dependências estão instaladas (pip install -r requirements.txt)")
        return False
    
    return True

if __name__ == "__main__":
    main()
