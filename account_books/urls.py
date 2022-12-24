from django.urls import path

from . import views

app_name = "account_books"

urlpatterns = [
    path('memos', views.MemoAPI.as_view()),
    path('memos/<int:memo_id>', views.MemoDetailAPI.as_view()),
    path('share/memos/<int:memo_id>', views.MemoShareAPI.as_view()),
]