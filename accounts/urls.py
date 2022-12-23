from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path('registration', views.RegisterAPI.as_view()),
    path('login', views.LoginAPI.as_view()),
]