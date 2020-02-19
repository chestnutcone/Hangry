from django.contrib import admin
from vendor.models import Vendor, Location, Meal


# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'tel', 'location')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('city',)


class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'vendor')


admin.site.register(Vendor, VendorAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Location, LocationAdmin)
