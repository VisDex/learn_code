from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse

EXEMPT_URLS = [settings.LOGIN_URL.lstrip('/')]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [url for url in settings.LOGIN_EXEMPT_URLS]


def process_view(request, view_func, view_args, view_kwargs):
    assert hasattr(request, 'user')
    path = request.path_info.lstrip('/')

    # if not request.user.is_authenticated:
    #     if not path in EXEMPT_URLS:
    #         return HttpResponseRedirect(settings.LOGIN_URL)

    url_is_exempt = [url for url in EXEMPT_URLS]
    if path == reverse('accounts:logout'.lstrip('/')):
        logout(request)
    if request.user.is_authenticated and url_is_exempt:
        return redirect(settings.LOGIN_REDIRECT_URL)

    elif request.user.is_authenticated or url_is_exempt:
        return None

    else:
        return redirect(settings.LOGIN_URL)


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
