from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sign_up", views.sign_up, name="sign_up"),
    path("sign_in", views.sign_in, name="sign_in"),
    path("read_user", views.read_user, name="read_user"),
    path("read_all_user", views.read_all_user, name="read_all_user")
]