from random import randint

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.home import services
import logging
from apps.authentication.tasks import send_verification_email, send_mail


@api_view(['GET', 'POST'])
def alive(request):
    send_mail.delay("sweetie.77@mail.ru", "НАЙС")


@api_view(["POST"])
def mail(request):
    email = request.POST['email']
    message = request.POST['message']
    send_mail.delay(email, message)
    return status.HTTP_202_ACCEPTED

@api_view(["POST"])
def messenger(request):
    number = request.POST['number']
    message = request.POST['message']
    result = services.send_message(number, message)
    return Response(status=result)

@api_view(["GET", "POST"])
def ping(request):
    return HttpResponse('pong')