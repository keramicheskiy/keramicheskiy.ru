import logging
import random
import sys

from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.authentication.models import CustomUser, VerifyCode
from apps.authentication.serializers import UserSerializer, CreateUserSerializer
from .authentication import CookieTokenAuthentication
from .decorators import verified_user, authenticated_user
from .services import verify_email


@api_view(['POST', 'GET'])
def register(request):
    if request.method == 'GET':
        return Response({"fields": CreateUserSerializer.Meta.fields})

    elif request.method == 'POST':
        print("Получены данные:", request.data)
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print("Пользователь сохранён:", user)
            token = Token.objects.create(user=user)
            print("Токен создан:", token.key)
            verify_email(user)
            print("verify_email вызван")

            response = Response({
                'token': token.key,
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)

            return response
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
{
"username": "keramicheskiy",
"email": "info@keramicheskiy.com",
"password": "nigga"
}
"""


@api_view(['POST'])
def login(request):
    user = get_object_or_404(CustomUser, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response("missing user", status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    response = Response({'token': token.key, 'user': serializer.data})
    response.set_cookie(
        "Token",
        token.key,
        max_age=60 * 60 * 24 * 30,  # 30 дней
        httponly=True,  # Чтобы JS не мог просто так достать токен
        samesite="Lax",  # Защита от CSRF
    )
    return response


@api_view(['GET'])
# @authentication_classes([SessionAuthentication, TokenAuthentication])
@authentication_classes([CookieTokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response(f"passed for {request.user.username}, token: {request.COOKIES.get('Token')}",
                    status=status.HTTP_200_OK)


@api_view(['GET'])
@verified_user
@authenticated_user
def test_token_1(request):
    return Response(f"passed for {request.user.username}, token: {request.COOKIES.get('Token')}",
                    status=status.HTTP_200_OK)


'''
{
"username": "krmch",
"email": "Sweetie.77@mail.ru",
"password": "Sagay228"
}
'''
