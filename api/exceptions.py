from django.http import Http404
from rest_framework.exceptions import (NotFound, NotAuthenticated, AuthenticationFailed, PermissionDenied,
                                       ValidationError)
from rest_framework.views import exception_handler
from .utils import error


def handler(exc, ctx):
    if isinstance(exc, (NotAuthenticated, AuthenticationFailed, PermissionDenied)):
        return error('Forbidden for you', status=403)
    if isinstance(exc, ValidationError):
        return error('Invalid fields', exc.detail, status=422)
    if isinstance(exc, (NotFound, Http404)):
        return error('Not found', status=404)
    return exception_handler(exc, ctx)
