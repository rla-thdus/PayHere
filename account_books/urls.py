from django.urls import path

from . import views

app_name = "account_books"

urlpatterns = [
    path('memos', views.MemoAPI.as_view()),
]