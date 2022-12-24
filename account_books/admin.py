from django.contrib import admin

from account_books.models import Memo, Url


@admin.register(Memo)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'spend_price', 'content', 'created_at', 'updated_at', 'deleted_at']


@admin.register(Url)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'memo', 'expired_at', 'updated_at', 'link']