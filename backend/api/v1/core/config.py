import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente a partir da raiz do projeto
# BASE_DIR resolvido primeiro, depois usamos para localizar o .env

# Configurações da aplicação
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
# No Heroku, variáveis de ambiente são definidas diretamente, não via .env
# Mas carrega .env se existir (para desenvolvimento local)
env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)
EXCEL_FILE = "quotes_data.xlsx"

# Configurações do Banco de Dados
DATABASE_URL = os.getenv("DATABASE_URL")

# Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Configurações de CORS
CORS_ORIGINS = ["*"]  # Em produção, especifique os domínios permitidos
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["*"]
CORS_ALLOW_HEADERS = ["*"]

# Configurações da API
API_TITLE = "API de Orçamentos Residenciais"
API_DESCRIPTION = "API REST para gerenciamento de orçamentos residenciais com banco de dados MySQL"
API_VERSION = "1.0.0"
