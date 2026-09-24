from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class BearerAuth(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except AuthenticationFailed:
            return None