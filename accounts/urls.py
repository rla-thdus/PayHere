from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.RegisterAPI.as_view()),
    path('login', views.LoginAPI.as_view()),
    path('logout', views.LogoutAPI.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('token/verify', TokenVerifyView.as_view()),
]