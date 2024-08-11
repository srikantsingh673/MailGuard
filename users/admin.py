from django.contrib import admin
from .models import Users

class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'full_name', 'mobile', 'is_staff', 'is_active']

admin.site.register(Users, UsersAdmin)
