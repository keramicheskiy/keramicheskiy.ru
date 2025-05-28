import requests
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from . import forms
from frontend.settings import BACKEND_URL


def register(request):
    if request.method == 'GET':
        return render(request, "authentication/registration.html",
                      context={"form": forms.RegistrationForm})
    elif request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            result = requests.post(url=BACKEND_URL + "/auth/register", json=form.cleaned_data)
            if result.status_code == 201:
                token = result.json()['token']
                redirection = redirect(to="/profile")
                redirection.set_cookie(
                    "Token",
                    token.key,
                    max_age=60 * 60 * 24 * 30,
                    httponly=True,
                    samesite="Lax",
                )
                return redirection
            return HttpResponse(f"{result.status_code}, {result.text}")
        return HttpResponse(form.errors, status=400)


"""
{
"username": "keramicheskiy",
"email": "info@keramicheskiy.com",
"password": "nigga"
}
"""


def login(request):
    if request.method == 'GET':
        return render(request, "authentication/login.html", context={"form": forms.LoginForm})
    elif request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            result = requests.post(url=BACKEND_URL + "/auth/login", data=form.cleaned_data)
            if result.status_code == 200:
                token = result.json()['token']
                redirection = redirect(to="/profile")
                redirection.set_cookie(
                    "Token",
                    token.key,
                    max_age=60 * 60 * 24 * 30,
                    httponly=True,
                    samesite="Lax",
                )
                return redirection
            return HttpResponse(result.status_code)
        return HttpResponse(form.errors, status=400)


# @api_view(['GET'])
# # @authentication_classes([SessionAuthentication, TokenAuthentication])
# @authentication_classes([CookieTokenAuthentication])
# @permission_classes([IsAuthenticated])
# def test_token(request):
#     return Response(f"passed for {request.user.username}, token: {request.COOKIES.get('Token')}",
#                     status=status.HTTP_200_OK)
#
#
# @api_view(['GET'])
# @verified_user
# @authenticated_user
# def test_token_1(request):
#     return Response(f"passed for {request.user.username}, token: {request.COOKIES.get('Token')}",
#                     status=status.HTTP_200_OK)


'''
{
"username": "krmch",
"email": "Sweetie.77@mail.ru",
"password": "Sagay228"
}
'''
