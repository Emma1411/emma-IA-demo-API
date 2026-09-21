import logging

from fastapi import APIRouter, Request

from config.settings import settings
from middlewares.rate_limit import limiter
from models.chat_schemas import ChatRequest, ChatResponse
from services.emma_client import appeler_emma_chat


# Initialise le logger du module
logger = logging.getLogger(__name__)

# Crée le router FastAPI
router = APIRouter()


@router.post("/api/chat", response_model=ChatResponse)
@limiter.limit(settings.rate_limit_demo)
async def chat(request: Request, payload: ChatRequest):
    # Reçoit la requête du frontend et la transmet à Emma IA
    resultat = await appeler_emma_chat(payload.model_dump())

    # Retourne la réponse d'Emma IA au frontend
    return resultat
