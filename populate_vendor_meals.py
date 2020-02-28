# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 22:31:43 2020

@author: Oliver
"""

import os, django
import pickle

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "food_ordering.settings")
django.setup()

from vendor.models import Vendor, Meal

with open('vendor_populate.pickle', 'rb') as f:
    vendors_info = pickle.load(f)

vendor_keys = list(vendors_info.keys())
for v in vendor_keys:    
    cur_vendor_info = vendors_info[v]
    vendor = Vendor.objects.get_or_create(name=v,
                               tel=cur_vendor_info['Tel'],
                               city=cur_vendor_info['City'],
                               street_address=cur_vendor_info['Street Address'])
    for meal in cur_vendor_info['meal']:
        new_meal = Meal.objects.get_or_create(name=meal[0],
                                      vendor=vendor[0],
                                      price=meal[1])
        