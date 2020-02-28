from django.contrib import admin
from people.models import Employee


# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('get_team', 'get_name', 'balance', 'get_email')

    def get_name(self, indv):
        return str(indv)

    def get_email(self, indv):
        return indv.user.email

    def get_team(self, indv):
        return str(indv.user.team)


admin.site.register(Employee, EmployeeAdmin)