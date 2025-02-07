from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),

    path("password_recovery/", views.password_recovery, name="password_recovery"),
    path("send_otp/", views.send_otp, name="send_otp"),
    path("reset-password/", views.reset_password, name="reset_password"),
]
