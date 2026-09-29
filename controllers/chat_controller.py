import logging

from fastapi import APIRouter, Request

from models.chat_schemas import ChatRequest, ChatResponse
from services.emma_client import appeler_emma_chat


# Initialise le logger du module
logger = logging.getLogger(__name__)

# Crée le router FastAPI
router = APIRouter()


@router.post("/api/chat", response_model=ChatResponse)
async def chat(request: Request, payload: ChatRequest):
    # Reçoit la requête du frontend et la transmet à Emma IA.
    # Aucune limite de débit ici — retirée pour que personne ne
    # butte sur un 429 en testant la démo publique.
    resultat = await appeler_emma_chat(payload.model_dump())

    # Retourne la réponse d'Emma IA au frontend
    return resultat