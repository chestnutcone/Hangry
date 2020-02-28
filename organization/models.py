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
                                 on_delete=models.SET_NULL,
                                 null=True)

    # only allow one instance
    def save(self, *args, **kwargs):
        if not self.pk and Organization.objects.exists():
            raise ValidationError("There can only be one Organization instance")
        return super(Organization, self).save(*args, **kwargs)

    @staticmethod
    def get_organization_timezone():
        try:
            org = Organization.objects.all()[0]  # only one can exist
        except IndexError:
            org = Organization.objects.create(name='default_org_name')
        timezone = org.timezone
        if timezone is None:
            timezone = 'America/Vancouver'
        timezone = pytz.timezone(str(timezone))
        return timezone

    @staticmethod
    def convert_to_utc(time):
        """time is datetime.date without timezone info"""
        timezone = Organization.get_organization_timezone()
        time = datetime.datetime(time.year, time.month, time.day).astimezone(timezone)
        time = time.astimezone(pytz.utc)  # register as UTC time
        return time

    @staticmethod
    def get_today_start_utc():
        today = datetime.datetime.now().date()
        return Organization.convert_to_utc(today)

