# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 18:35:02 2023

@author: furka
"""

import pandas as pd

df = pd.read_csv("maaslar.csv")

x = df.iloc[:, :1]
y = df.iloc[:, 1:]

import sklearn