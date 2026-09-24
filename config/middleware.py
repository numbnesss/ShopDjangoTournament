from django.utils import translation


class ApiLocaleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, req):
        if req.path.startswith('/api/'):
            with translation.override('en-US'):
                return self.get_response(req)
        return self.get_response(req)
