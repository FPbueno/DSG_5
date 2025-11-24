#!/bin/bash
# Wrapper script para executar testes configurando o PYTHONPATH corretamente
set -e

# Navega para o diretório backend (caso não esteja lá)
cd "$(dirname "$0")"

# Configura PYTHONPATH
export PYTHONPATH="$(pwd):$PYTHONPATH"

# Executa pytest com os argumentos passados
exec python -m pytest "$@"

