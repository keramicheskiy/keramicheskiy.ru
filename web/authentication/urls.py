from django.urls import path

from authentication import views

urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('test_token', views.test_token),
]