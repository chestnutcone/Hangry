# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 11:41:36 2020

@author: Oliver
"""

import pandas as pd
import os, django
import pickle
import json


# clean data, make it a dictionary
vendors_info = pd.read_csv("vendor.csv")
vendors_info.index = vendors_info['Name']
vendors_info.drop("Name", inplace=True, axis=1)
vendors_info = vendors_info.apply(lambda x: x.map(lambda x: x.strip()))
vendor_dict = vendors_info.T.to_dict()

meals_info = pd.read_csv("meal_info.csv")
meals_info['Meal'] = meals_info['Meal'].map(lambda x: x.strip())
meals_info['Name'] = meals_info['Name'].map(lambda x: x.strip())

vendor_meal_dict = {}
def add_meals_to_vendor(row):
    obj = vendor_meal_dict.get(row[0])
    if obj:
        obj.append((row[1], row[2]))
    else:
        vendor_meal_dict[row[0]] = [(row[1], row[2])]
    
meals_info.apply(add_meals_to_vendor, axis=1)

vendors = list(vendor_dict.keys())
for v in vendors:
    vendor_dict[v]['meal'] = vendor_meal_dict[v]
    
with open('vendor_populate.pickle', 'wb') as f:
    pickle.dump(vendor_dict, f)