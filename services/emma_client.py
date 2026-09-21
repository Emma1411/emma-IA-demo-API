import logging
import httpx
from fastapi import HTTPException
from config.settings import settings


# Initialise le logger du module
logger = logging.getLogger(__name__)


async def appeler_emma_chat(payload: dict) -> dict:
    try:
        # Crée un client HTTP asynchrone avec le timeout configuré
        async with httpx.AsyncClient(
            timeout=settings.emma_timeout_secondes
        ) as client:

            # Envoie le payload au endpoint Démo d'Emma IA
            r = await client.post(
                f"{settings.emma_ia_base_url}/api/v1/demo/chat",
                json=payload,
                headers={
                    # La clé API reste uniquement côté serveur
                    "X-API-Key": settings.api_key_demo,

                    # Identifie cette requête comme provenant du backend Démo
                    "X-Client-Type": "demo",

                    # Indique que le corps de la requête est en JSON
                    "Content-Type": "application/json",
                },
            )

            # Déclenche une exception pour les réponses HTTP en erreur
            r.raise_for_status()

            # Retourne la réponse JSON d'Emma IA au controller
            return r.json()

    except httpx.TimeoutException:
        # Gère le dépassement du délai d'attente
        logger.exception("Timeout en appelant Emma IA")

        raise HTTPException(
            status_code=504,
            detail="Emma IA ne répond pas — réessayez.",
        )

    except httpx.HTTPStatusError as exc:
        # Enregistre l'erreur HTTP retournée par Emma IA
        logger.warning(
            "Emma IA a retourné une erreur %s : %s",
            exc.response.status_code,
            exc.response.text,
        )

        # Transmet une erreur 429 lorsque la limite de requêtes est atteinte
        if exc.response.status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="Trop de requêtes — patientez un instant.",
            )

        # Transforme les autres erreurs HTTP en erreur 502
        raise HTTPException(
            status_code=502,
            detail="Emma IA a retourné une erreur.",
        )

    except httpx.RequestError:
        # Gère les erreurs réseau ou de connexion
        logger.exception("Erreur réseau en appelant Emma IA")

        raise HTTPException(
            status_code=502,
            detail="Impossible de contacter Emma IA.",
        )
