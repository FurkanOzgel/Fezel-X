# -*- coding: utf-8 -*-

import pandas as pd

sector_average_df = pd.read_csv("sector_average_df.csv", index_col=0)
share_ratio_df = pd.read_csv("share_ratio_df_06-2023.csv", index_col=0)
share_sector_df = pd.read_csv("share_sector_df.csv", index_col=0)
point_df = pd.read_csv("point_df_06-2023s.csv", index_col=0)
