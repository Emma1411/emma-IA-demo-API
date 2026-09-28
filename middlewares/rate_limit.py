from slowapi import Limiter
from starlette.requests import Request


def obtenir_ip_reelle(request: Request) -> str:

    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "inconnu"


limiter = Limiter(key_func=obtenir_ip_reelle)