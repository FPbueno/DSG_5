#!/usr/bin/env python3
"""
Script para testar o endpoint diretamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.v1.services.orcamento_service import listar_orcamentos_prestador
from api.v1.core.database import get_db
import json

def test_endpoint():
    """Testa o endpoint diretamente"""
    db = next(get_db())
    orcamentos = listar_orcamentos_prestador(db, 1)
    
    resultado = []
    for orc in orcamentos:
        resultado.append({
            "id": orc.id,
            "solicitacao_id": orc.solicitacao_id,
            "prestador_id": orc.prestador_id,
            "valor_ml_minimo": orc.valor_ml_minimo,
            "valor_ml_sugerido": orc.valor_ml_sugerido,
            "valor_ml_maximo": orc.valor_ml_maximo,
            "valor_proposto": orc.valor_proposto,
            "prazo_execucao": orc.prazo_execucao,
            "observacoes": orc.observacoes,
            "condicoes": orc.condicoes,
            "status": orc.status.value,
            "created_at": orc.created_at.isoformat() if orc.created_at else None,
            "prestador_nome": orc.prestador.nome,
            "prestador_avaliacao": orc.prestador.avaliacao_media,
            "categoria": orc.solicitacao.categoria,
            "descricao": orc.solicitacao.descricao
        })
    
    print("Resultado do endpoint:")
    print(json.dumps(resultado[0], indent=2, ensure_ascii=False))
    
    # Verificar se categoria e descricao estão presentes
    if 'categoria' in resultado[0] and 'descricao' in resultado[0]:
        print("\n✅ Campos categoria e descricao estão presentes!")
    else:
        print("\n❌ Campos categoria e descricao NÃO estão presentes!")

if __name__ == "__main__":
    test_endpoint()

