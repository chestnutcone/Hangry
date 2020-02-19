from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import CustomUser, Group

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'group')

admin.site.register(CustomUser, CustomUserAdmin)