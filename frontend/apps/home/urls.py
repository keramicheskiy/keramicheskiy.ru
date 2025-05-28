from django.urls import path

from . import views

urlpatterns = [
    path('', views.home),
    path('health', views.ping),
    path('1000-7', views.dead_inside),
    path('ping', views.ping),
    path('messenger', views.messenger),
]
