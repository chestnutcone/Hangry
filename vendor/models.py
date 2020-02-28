from django.db import models


# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=50)
    tel = models.CharField(max_length=15, unique=True)
    street_address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=50, null=False)

    def json_format(self):
        return {'name': self.name,
                'tel': self.tel,
                'city': self.city,
                'address': str(self.street_address+" "+self.city),
                'pk':self.pk}

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=15)
    vendor = models.ForeignKey(Vendor,
                               on_delete=models.CASCADE,
                               null=True)
    price = models.FloatField(default=0)

    def json_format(self):
        return {'name': self.name,
                'vendor': str(self.vendor),
                'price': str(self.price),
                'pk': self.pk}

    @staticmethod
    def get_vendor_meals(vendor_pk):
        if vendor_pk:
            vendor = Vendor.objects.get(pk=int(vendor_pk))
            meals = Meal.objects.filter(vendor=vendor)
            meals = [m.json_format() for m in meals]
            return meals
        return []

    def __str__(self):
        return self.vendor.name+" "+self.name
