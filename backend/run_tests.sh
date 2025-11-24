#!/bin/bash
# Wrapper script para executar testes configurando o PYTHONPATH corretamente
set -e

# Navega para o diretório backend (caso não esteja lá)
cd "$(dirname "$0")"

# Configura PYTHONPATH de forma explícita
CURRENT_DIR=$(pwd)
export PYTHONPATH="${CURRENT_DIR}:${PYTHONPATH}"

# Executa pytest com os argumentos passados
# O PYTHONPATH já está configurado acima
exec python -m pytest "$@"

