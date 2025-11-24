# Configura o PYTHONPATH antes de qualquer importação
import sys
import os
from pathlib import Path

# Adiciona o diretório atual ao sys.path se não estiver lá
# Isso é necessário para que os imports funcionem no Heroku
current_dir = Path(__file__).parent.absolute()
current_dir_str = str(current_dir)
if current_dir_str not in sys.path:
    sys.path.insert(0, current_dir_str)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa config com fallback robusto
try:
    from api.v1.core.config import (
        API_TITLE, API_DESCRIPTION, API_VERSION,
        CORS_ORIGINS, CORS_ALLOW_CREDENTIALS, 
        CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS
    )
except (ImportError, ModuleNotFoundError):
    # Valores padrão se config não estiver disponível
    API_TITLE = os.getenv("API_TITLE", "API de Orçamentos Residenciais")
    API_DESCRIPTION = os.getenv("API_DESCRIPTION", "API REST para gerenciamento de orçamentos residenciais")
    API_VERSION = os.getenv("API_VERSION", "1.0.0")
    CORS_ORIGINS = ["*"]
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]

from api.v1.routes import router
from api.v1.core.database import create_tables
from api.v1.core.security import generate_rsa_keys

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# Configuração do CORS para permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=CORS_ALLOW_METHODS,
    allow_headers=CORS_ALLOW_HEADERS,
)

# Inicialização não bloqueante para evitar timeout no Heroku
@app.on_event("startup")
async def startup_event():
    # Operações de inicialização são feitas sob demanda ou em background
    # para garantir que a aplicação responda rapidamente (< 20s no Heroku)
    pass

# Inclui as rotas
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "API de Orçamentos Residenciais funcionando!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
