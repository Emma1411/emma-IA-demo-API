# Backend Démo — Emma IA

Backend intermédiaire entre le front public de démonstration et emma-ia-service.
Ce service expose une **API publique limitée et stateless** permettant à un visiteur de tester les capacités conversationnelles et analytiques d'Emma IA à partir d'un dossier financier fourni dans la requête.
Le Backend Démo **ne prend aucune décision de crédit**, **ne calcule aucune métrique financière officielle** et **ne conserve aucune donnée** entre deux requêtes.
Il agit exclusivement comme une couche de **validation**, de **sécurité**, de **limitation de débit** et de **relais** entre le navigateur et emma-ia-service.

## Positionnement

Emma IA est un outil d'**assistance à l'analyse et à la décision**.
Elle analyse, structure, explique et signale les éléments présents dans les données qui lui sont transmises. Elle ne constitue **jamais** un système de décision autonome.
Toute appréciation produite par Emma IA reste soumise à la **validation d'un analyste humain**.
Le Backend Démo ne modifie pas cette logique : il transmet les données fournies par le visiteur à emma-ia-service et retourne sa réponse.


## Rôle exact du Backend Démo

Le Backend Démo a **cinq responsabilités principales** :

1. Recevoir les données et l'historique de conversation envoyés par le front
2. Valider la structure et les limites du payload avec **Pydantic**
3. Transmettre la requête à `emma-ia-service` avec la **clé API conservée côté serveur**
4. Appliquer une **limitation de débit** indépendante
5. **Uniformiser** les erreurs réseau et les erreurs provenant du service Emma IA

## Ce qu'il ne possède pas

- Aucune base de données
- Aucun système de session
- Aucun stockage de conversation
- Aucun cache
- Aucun utilisateur authentifié
- Aucune logique de décision de crédit
- Aucun calcul de métrique officielle

> L'état de la conversation appartient **entièrement au front**.


## Stack technique

- Python 3.11
- FastAPI
- Pydantic / Pydantic Settings — validation et configuration
- Uvicorn — serveur ASGI
- HTTPX — appels HTTP vers Emma IA
- SlowAPI — rate limiting
- CORS Middleware — contrôle des origines autorisées
- OpenAPI / Swagger — documentation de l'API
- Docker — conteneurisation
- Render — déploiement
- .env — configuration et secrets côté serveur

## Architecture

```
                         INTERNET
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Front Démo Public   │
                 │ React / navigateur  │
                 │                     │
                 │ useState            │
                 │ messages[]          │
                 │ dossier             │
                 └──────────┬──────────┘
                            │
                            │ HTTPS
                            ▼
                 ┌─────────────────────┐
                 │ Backend Démo        │
                 │ FastAPI             │
                 │                     │
                 │ POST /api/chat      │
                 │ GET  /api/health    │
                 │                     │
                 │ Validation          │
                 │ CORS                │
                 │ Rate limiting       │
                 │ Gestion erreurs     │
                 └──────────┬──────────┘
                            │
                            │ X-API-Key
                            │ X-Client-Type: demo
                            │
                            ▼
              ┌─────────────────────────────┐
              │       Emma IA Service       │
              │                             │
              │ /api/v1/demo/chat           │
              │                             │
              │ Chat stateless Démo         │
              │ Analyse                     │
              │ Validation                  │
              │ Garde-fous métier           │
              │ DeepSeek                    │
              └─────────────────────────────┘
```

Le Backend Démo n'est **pas une deuxième implémentation d'Emma IA**.
Il constitue une **façade sécurisée et publique** devant l'API Démo de `emma-ia-service`.