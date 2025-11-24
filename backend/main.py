from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes import router
from api.v1.core.config import (
    API_TITLE, API_DESCRIPTION, API_VERSION,
    CORS_ORIGINS, CORS_ALLOW_CREDENTIALS, 
    CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS
)
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

# Cria as tabelas do banco de dados na inicialização
@app.on_event("startup")
async def startup_event():
    try:
        create_tables()
    except Exception:
        pass
    try:
        generate_rsa_keys()
    except Exception:
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
