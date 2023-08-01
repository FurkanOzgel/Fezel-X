#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 15:52:51 2023

@author: furkan
"""

import pandas as pd

examine_df = pd.read_csv("examine_df.csv")

x = examine_df[[ "Now", "Prediction"]]
y = examine_df["Succes"]