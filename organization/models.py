from django.db import models
from django.core.exceptions import ValidationError
import datetime
import pytz


class Timezone(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=50)
    timezone = models.ForeignKey(Timezone,
                                 on_delete=models.CASCADE,
                                 default=195)

    # only allow one instance
    def save(self, *args, **kwargs):
        if not self.pk and Organization.objects.exists():
            raise ValidationError("There can only be one Organization instance")
        return super(Organization, self).save(*args, **kwargs)

    @staticmethod
    def convert_to_utc(time):
        """time is datetime.date without timezone info"""
        timezone = Organization.objects.all()[0].timezone  # only one can exist
        timezone = pytz.timezone(str(timezone))
        time = datetime.datetime(time.year, time.month, time.day).astimezone(timezone)
        time = time.astimezone(pytz.utc)  # register as UTC time
        return time

    @staticmethod
    def get_today_start_utc():
        today = datetime.datetime.now().date()
        return Organization.convert_to_utc(today)

