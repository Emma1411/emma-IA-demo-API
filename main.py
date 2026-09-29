from contextlib import asynccontextmanager
from fastapi import FastAPI
from controllers.chat_controller import router as chat_router
from controllers.health_controller import router as health_router
from middlewares.cors import appliquer_cors
from utils.logger import configurer_logging


# Configure les logs de l'application
configurer_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Aucun service persistant n'est nécessaire au démarrage
    # Le client HTTP est créé et fermé pour chaque requête
    yield


# Initialise l'application FastAPI
app = FastAPI(
    title="SecureFinance-RAG — Backend Démo",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
)


# Configure le CORS de l'application
appliquer_cors(app)


# Enregistre les routes du chat
app.include_router(chat_router)

# Enregistre la route de healthcheck
app.include_router(health_router)