from django.utils import translation


class KzUrlLocaleMiddleware:
    """Use /kz/ as the public URL prefix while keeping Django's Kazakh code as kk."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        force_kazakh = request.path_info == "/kz" or request.path_info.startswith("/kz/")
        if force_kazakh:
            translation.activate("kk")
            request.LANGUAGE_CODE = "kk"

        response = self.get_response(request)

        if force_kazakh:
            response.headers["Content-Language"] = "kk"

        return response
