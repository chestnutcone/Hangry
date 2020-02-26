from django.db import models
from django.contrib.auth.models import AbstractUser
from vendor.models import Vendor


# Create your models here.
class CustomUser(AbstractUser):
    team = models.ForeignKey("Team",
                             on_delete=models.SET_NULL,
                             null=True,
                             )

    def json_format(self):
        return {'name': str(self),
                'email': self.username,
                'pk': str(self.pk)}

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Team(models.Model):
    name = models.CharField(max_length=20)
    executor = models.ForeignKey(CustomUser,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='team_executor')
    vendors = models.ManyToManyField(Vendor)

    def __str__(self):
        return self.name
