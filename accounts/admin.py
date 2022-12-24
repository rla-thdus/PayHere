from django.contrib import admin

from accounts.models import User


@admin.register(User)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'created_at']