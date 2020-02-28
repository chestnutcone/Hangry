from django.contrib import admin
from vendor.models import Vendor, Meal


# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'tel', 'street_address')

class MealAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'name', 'price')


admin.site.register(Vendor, VendorAdmin)
admin.site.register(Meal, MealAdmin)
