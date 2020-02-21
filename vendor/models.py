from django.db import models


# Create your models here.
class Location(models.Model):
    city = models.CharField(max_length=15)

    def __str__(self):
        return self.city


class Vendor(models.Model):
    name = models.CharField(max_length=30)
    tel = models.CharField(max_length=15, unique=True)
    location = models.ForeignKey(Location,
                                 on_delete=models.SET_NULL,
                                 null=True)
    address = models.CharField(max_length=30, unique=True)

    def json_format(self):
        return {'name': self.name,
                'tel': self.tel,
                'location': self.location.city,
                'address': self.address,
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

    def __str__(self):
        return self.vendor.name+" "+self.name
