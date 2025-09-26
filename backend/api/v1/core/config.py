import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv('.env')

# Configurações da aplicação
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
EXCEL_FILE = "quotes_data.xlsx"

# Configurações do Banco de Dados
DATABASE_URL = os.getenv(
    "DATABASE_URL"
)

# Configurações de CORS
CORS_ORIGINS = ["*"]  # Em produção, especifique os domínios permitidos
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# Configurações da API
API_TITLE = "API de Orçamentos Residenciais"
API_DESCRIPTION = "API REST para gerenciamento de orçamentos residenciais com banco de dados MySQL"
API_VERSION = "1.0.0"
