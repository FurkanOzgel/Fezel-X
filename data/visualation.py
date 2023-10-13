#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 21:33:59 2023

@author: furkan
"""

import pandas as pd

price_increase_22_12 = pd.read_csv("2022-12/price_increase_df.csv",
                                       index_col= 0)
price_increase_23_3 = pd.read_csv("2023-3/price_increase_df.csv",
                                       index_col= 0)

