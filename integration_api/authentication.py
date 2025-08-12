from rest_framework import authentication, exceptions
from django.conf import settings

class APIKeyAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get("X-API-KEY")
        if not api_key:
            return None  
        if api_key != settings.EXTERNAL_API_KEY:
            raise exceptions.AuthenticationFailed("Chave de API inválida.")
        return (None, None)
