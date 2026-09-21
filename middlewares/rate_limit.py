from slowapi import Limiter
from slowapi.util import get_remote_address


# Limite les requêtes en fonction de l'adresse IP du client
# Cette limite protège le backend démo
# Emma IA applique également sa propre limite en aval
limiter = Limiter(key_func=get_remote_address)
