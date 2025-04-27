from django.shortcuts import render, get_object_or_404

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import CustomUser
from authentication.serializers import UserSerializer, CreateUserSerializer
from .authentication import CookieTokenAuthentication


# Create your views here.


@api_view(['POST', 'GET'])
def register(request):
    if request.method == 'GET':
        return Response({"fields": CreateUserSerializer.Meta.fields})
    elif request.method == 'POST':
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = CustomUser.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': UserSerializer(user).data})
        return Response(serializer.errors, status=status.HTTP_200_OK)


"""
{
"username": "krmch",
"email": "sweetie.77@mail.ru",
"password": "Sagay228"
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
    return Response(f"passed for {request.user.username}, token: {request.COOKIES.get('Token')}", status=status.HTTP_200_OK)
