from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from home import forms, services
import logging


# Create your views here.
@api_view(["GET"])
def dead_inside(request):
    return render(request, "1000-7.html")


@api_view(["POST", "GET"])
def messager(request):
    if request.method == "GET":
        data = {
            "form": forms.MessageForm(),
        }
        return render(request, "message.html", context=data)
    elif request.method == "POST":
        form = forms.MessageForm(request.POST)
        if form.is_valid():
            try:
                number = form.cleaned_data["number"]
                message = form.cleaned_data["message"]
                result = services.send_message(number, message)
                return HttpResponse(result)
            except Exception as e:
                logger = logging.getLogger()
                logger.warning(str(e))
                return HttpResponse(str(e))
        return HttpResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def ping(request):
    return HttpResponse("pong")


@api_view(["GET"])
def home(request):



    return render(request, "authentication/registration.html")