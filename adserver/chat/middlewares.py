from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from django.db import close_old_connections


class DialogueMiddleWare:

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        headers = dict(scope['headers'])

        if b'authorization' in headers:
            try:
                token_name, token_key = headers[b'authorization'].decode().split(' ')
                if token_name == 'Token':
                    token = Token.objects.get(key=token_key)
                    scope['user'] = token.user
                    close_old_connections()
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser
        return self.inner(scope)