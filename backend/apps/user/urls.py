from django.urls import path
from . import views

urlpatterns = [
    path("verify", views.verify),
    path("resend_verification_code", views.resend_verification_code),
    path("<username>", views.profile),
    path("", views.redirect_to_profile),

]