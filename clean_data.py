# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 11:41:36 2020

@author: Oliver
"""

import pandas as pd

fname = 'fourth.csv'

df = pd.read_csv(fname)
df['Price'] = df['Price'].map(lambda x: x.split("$")[1])
df['Vendor'] = df['Vendor'].map(lambda x: x.strip())
df.to_csv(fname)

import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "food_ordering.settings")
django.setup()

from vendor.models import Vendor, Meal

fnames = ['first.csv', 'second.csv', 'third.csv', 'fourth.csv']
vendors = Vendor.objects.all()

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
for i in range(len(fnames)):
    df = pd.read_csv(fnames[i])
    tpl = [tuple(x) for x in df.to_numpy()]
    vendor = vendors[i]
    for meal, price in tpl:  
        new_meal = Meal(name=meal,
                        vendor=vendor,
                        price=float(price))
        new_meal.save()
        

