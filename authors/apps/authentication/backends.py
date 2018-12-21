import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User

"""Configure JWT Here"""

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        """
        Determines if the current user making the request isauthenticated
        """

        expected_prefix = settings.JWT['TOKEN_PREFIX'].lower()
        request.user = None
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_len = len(auth_header)
        if not auth_header or auth_header_len != 2:
            return None
        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")

        if prefix.lower() != expected_prefix:
            return None # pragma: no cover

        return self._get_user_credentials_from_token(token)

    def _get_user_credentials_from_token(self, token):
        """Extracts a user from a  JSON web token"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except Exception: # pragma: no cover
            raise exceptions.AuthenticationFailed("Failed decoding token") # pragma: no cover

        try:
            user = User.objects.get(username=payload['username'])
        except User.DoesNotExist:# pragma: no cover
            raise exceptions.AuthenticationFailed( # pragma: no cover
                "The provided token doesnot belong to any user"
            )
        if not user.is_active:
            raise exceptions.AuthenticationFailed( # pragma: no cover
                "The users profile has been deactivated"
            )
        # at this point we are sure we have the user
        return (user, token)
