from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.routes import router
from api.v1.core.config import (
    API_TITLE, API_DESCRIPTION, API_VERSION,
    CORS_ORIGINS, CORS_ALLOW_CREDENTIALS, 
    CORS_ALLOW_METHODS, CORS_ALLOW_HEADERS
)

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

# Inclui as rotas
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "API de Itens funcionando!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
