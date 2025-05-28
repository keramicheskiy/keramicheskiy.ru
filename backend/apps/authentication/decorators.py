from django.shortcuts import redirect
from rest_framework.authtoken.models import Token


def authenticated_user(function):
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('Token')
        if not token:
            return redirect("/auth/login")
        return function(request, *args, **kwargs)

    return wrapper


def verified_user(function):
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('Token')
        try:
            user = Token.objects.get(key=token).user
        except Token.DoesNotExist:
            return redirect("/auth/login")

        if not user.is_verified:
            return redirect("/profile/verify")

        return function(request, *args, **kwargs)

    return wrapper


# @verified_user
# @authenticated_user
# def main_page(request):
#     return render("main.html")
