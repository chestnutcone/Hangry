# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 22:24:55 2020

@author: Oliver
"""

import os, django
import pytz

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "food_ordering.settings")
django.setup()

# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
common_timezones = list(pytz.common_timezones)
common_timezones.remove('GMT')
common_timezones.remove('UTC')

from organization.models import Timezone
for tz in common_timezones:
    Timezone.objects.create(name=tz.strip())
