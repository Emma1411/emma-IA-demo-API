import httpx
from fastapi import APIRouter
from config.settings import settings


# Crée le router FastAPI
router = APIRouter()


@router.get("/api/health")
async def health():
    # Indique si le service Emma IA est accessible
    emma_ok = False

    try:
        # Crée un client HTTP avec un timeout de 5 secondes
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Vérifie l'état du service Emma IA
            r = await client.get(
                f"{settings.emma_ia_base_url}/api/v1/health"
            )

            # Considère Emma IA comme disponible uniquement avec un statut 200
            emma_ok = r.status_code == 200

    except Exception:
        # Considère Emma IA comme indisponible en cas d'erreur
        emma_ok = False

    # Retourne l'état du backend et d'Emma IA
    return {
        "status": "ok" if emma_ok else "degraded",
        "emma_ia": "ok" if emma_ok else "unavailable",
    }
