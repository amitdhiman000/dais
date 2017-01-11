from django.utils.functional import SimpleLazyObject
from . import backends

def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = backends.get_user(request)
    return request._cached_user

class AuthMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), (
            "The Django authentication middleware requires session middleware "
            "to be installed. Edit your MIDDLEWARE_CLASSES setting to insert "
            "'django.contrib.sessions.middleware.SessionMiddleware' before "
            "'django.contrib.auth.middleware.AuthenticationMiddleware'."
        )
        request.user = SimpleLazyObject(lambda: get_user(request))
