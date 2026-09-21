from fastapi.middleware.cors import CORSMiddleware
from config.settings import settings


def appliquer_cors(app) -> None:
    # Autorise uniquement les domaines présents dans ALLOWED_ORIGINS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,

        # Aucun cookie ou session utilisateur n'est utilisé
        allow_credentials=False,

        # Autorise uniquement les méthodes HTTP nécessaires
        allow_methods=["GET", "POST"],

        # Autorise les headers nécessaires aux requêtes JSON
        allow_headers=["Content-Type"],
    )
