
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('Token')
        if not token:
            return None  # Нет токена в куках — значит, не аутентифицируем

        return self.authenticate_credentials(token)
