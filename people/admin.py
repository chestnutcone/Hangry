from django.contrib import admin
from people.models import Employee

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_email', 'balance')

    def get_name(self, indv):
        return str(indv)

    def get_email(self, indv):
        return indv.user.email


admin.site.register(Employee, EmployeeAdmin)