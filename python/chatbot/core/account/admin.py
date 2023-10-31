

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.account.models import CustomUser

# UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'uid', 'is_active', 'updated_at', 'created_at', 'is_verified']


admin.site.register(CustomUser, CustomUserAdmin)