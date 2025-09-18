import os
from pathlib import Path

# Configurações da aplicação
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
EXCEL_FILE = "quotes_data.xlsx"

# Configurações de CORS
CORS_ORIGINS = ["*"]  # Em produção, especifique os domínios permitidos
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# Configurações da API
API_TITLE = "API de Orçamentos Residenciais"
API_DESCRIPTION = "API REST para gerenciamento de orçamentos residenciais usando Excel como banco de dados"
API_VERSION = "1.0.0"
