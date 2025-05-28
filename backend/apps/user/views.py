from http.client import responses

from django.shortcuts import render, redirect
from kombu.asynchronous.http import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view

from apps.authentication.decorators import authenticated_user
from apps.authentication.models import CustomUser, VerifyCode
from django.shortcuts import get_object_or_404

from apps.authentication.services import verify_email


def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)

    return render(request, "user/profile.html", context={"user": user})


@authenticated_user
@api_view(['GET', 'POST'])
def verify(request):
    if request.method == 'GET':
        return render(request, "user/verification.html")
    elif request.method == 'POST':
        code = request.POST['code']
        token = request.COOKIES.get('Token')
        user = Token.objects.get(key=token).user
        verify_code = VerifyCode.objects.filter(code=code, user=user)
        if len(verify_code) != 0:
            for entry in verify_code:
                entry.delete()
            user.is_verified = True
            user.save()
            return redirect(f'/profile/{user.username}')
        return Response("Неправильный код.", status.HTTP_400_BAD_REQUEST)


@authenticated_user
@api_view(['GET'])
def resend_verification_code(request):
    token = request.COOKIES.get('token')
    user = Token.objects.get(key=token).user
    verify_email(user)
    return redirect('/profile/verify')


@authenticated_user
@api_view(['GET'])
def redirect_to_profile(request):
    token = request.COOKIES.get('token')
    user = Token.objects.get(key=token).user
    return redirect(f'/profile/{user.username}')