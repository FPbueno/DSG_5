#!/usr/bin/env python3
"""
Script para configurar e inicializar o banco de dados Supabase (PostgreSQL)
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório do projeto ao path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from api.v1.core.database import create_tables, engine
from api.v1.models.db_models import Cliente, Prestador, Solicitacao, Orcamento, Avaliacao

def main():
    """Função principal para configurar o banco de dados"""
    print("🔧 Configurando banco de dados Supabase (PostgreSQL)...")
    
    try:
        # Testa a conexão com o banco
        print("📡 Testando conexão com o Supabase...")
        connection = engine.connect()
        connection.close()
        print("✅ Conexão com o Supabase estabelecida com sucesso!")
        
        # Cria as tabelas
        print("📋 Criando tabelas no Supabase...")
        create_tables()
        print("✅ Tabelas criadas com sucesso!")
        
        print("\n🎉 Banco de dados Supabase configurado com sucesso!")
        print("📊 Tabelas disponíveis:")
        print("   - clientes (perfis de cliente)")
        print("   - prestadores (perfis de prestador)")
        print("   - solicitacoes (solicitações de orçamento)")
        print("   - orcamentos (orçamentos dos prestadores)")
        print("   - avaliacoes (avaliações dos serviços)")
        print("\n🚀 Você pode agora iniciar a API com: python main.py")
        
    except Exception as e:
        print(f"❌ Erro ao configurar o banco de dados: {e}")
        print("\n🔍 Verifique:")
        print("   1. Se as credenciais do Supabase estão corretas no .env")
        print("   2. Se o projeto Supabase está ativo")
        print("   3. Se as dependências estão instaladas (pip install -r requirements.txt)")
        print("   4. Se a senha do banco está correta")
        return False
    
    return True

if __name__ == "__main__":
    main()
