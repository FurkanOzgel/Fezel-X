#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 21:33:59 2023

@author: furkan
"""

import pandas as pd

price_increase_22_12 = pd.read_csv("data/2022-12/price_increase_df.csv",
                                       index_col= 0)
price_increase_23_3 = pd.read_csv("data/2023-3/price_increase_df.csv",
                                       index_col= 0)

ratio_df = pd.read_csv("data/2023-3/share_ratio_df_2023-3.csv",
                                       index_col= 0)

sector_average = pd.read_csv("data/2023-3/sector_average_df_2023-3.csv",
                                       index_col= 0)

