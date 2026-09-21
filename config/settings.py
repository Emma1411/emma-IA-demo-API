from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # URL de base du service Emma IA
    emma_ia_base_url: str = "http://localhost:8000"

    # Clé API utilisée uniquement côté serveur
    api_key_demo: str = ""

    # Liste des domaines autorisés à appeler l'API
    allowed_origins: list[str] = ["http://localhost:5173"]

    # Limite de requêtes pour le endpoint de démonstration
    rate_limit_demo: str = "10/minute"

    # Temps maximum d'attente lors d'un appel vers Emma IA
    emma_timeout_secondes: float = 30.0

    # Charge automatiquement les variables présentes dans .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


# Charge la configuration de l'application
settings = Settings()
