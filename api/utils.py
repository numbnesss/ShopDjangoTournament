from rest_framework.response import Response


def error(message, errors=None, status=422):
    body = {'message': message}
    if errors is not None:
        body['errors'] = errors
    return Response(body, status=status)
