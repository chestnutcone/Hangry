from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    group = models.ForeignKey("Group",
                              on_delete=models.SET_NULL,
                              null=True,
                              )

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Group(models.Model):
    name = models.CharField(max_length=20)
    executor = models.ForeignKey(CustomUser,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='group_executor')

    def __str__(self):
        return self.name
