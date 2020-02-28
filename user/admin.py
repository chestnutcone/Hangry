from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import CustomUser, Team
from user.forms import CustomUserCreationForm, CustomUserChangeForm


# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('team', 'first_name', 'last_name', 'email')


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_executor')

    @staticmethod
    def get_executor(team):
        return str(team.executor)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Team, TeamAdmin)