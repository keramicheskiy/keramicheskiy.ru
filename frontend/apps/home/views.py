from random import randint

from django.http import HttpResponse
from django.shortcuts import render

from . import forms
from frontend.settings import BACKEND_URL
import requests


def dead_inside(request):
    return render(request, "home/1000-7.html")


def messenger(request):
    if request.method == "GET":
        data = {"form": forms.MessageForm()}
        return render(request, "home/message.html", context=data)

    elif request.method == "POST":
        form = forms.MessageForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data["number"]
            message = form.cleaned_data["message"]
            result = requests.post(url=BACKEND_URL + "/messenger",
                                   data={"number": number, "message": message},
                                   cookies=request.COOKIES)
            return HttpResponse(result)

        return HttpResponse(form.errors, status=400)


def ping(request):
    return HttpResponse("pong")


def home(request):
    # send_verification_email.delay('sweetie.77@mail.ru', str(randint(0, 9999)).zfill(4))
    result = requests.post(url=BACKEND_URL + "/mail",
                           data={"email": "sweetie.77@mail.ru", "message": "hhh"},
                           cookies=request.COOKIES)
    return HttpResponse({"data": result.text})
