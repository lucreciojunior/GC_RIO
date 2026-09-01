"""Aplicação principal FastAPI - Backend Contagem RIO."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import auth, usuarios, igrejas, contagens

app = FastAPI(
    title="Contagem RIO - API",
    description="Backend do sistema de gestão de cultos da Igreja RIO.",
    version="1.0.0",
)

# CORS - permite o frontend acessar a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(igrejas.router)
app.include_router(contagens.router)


@app.get("/", tags=["Status"])
def raiz():
    """Endpoint de verificação de saúde da API."""
    return {
        "app": "Contagem RIO - API",
        "status": "online",
        "docs": "/docs",
    }


@app.get("/health", tags=["Status"])
def health():
    return {"status": "ok"}
