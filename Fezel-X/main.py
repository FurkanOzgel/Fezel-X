import ratioDf
from analyzer import Analyzer

# ratioDf.create_share_ratio_df()
# ratioDf.update_share_ratio_df()
# ratioDf.create_share_sector_df()
# ratioDf.update_share_sector_df()
# ratioDf.produce_sector_average_df()

# Analyzer(config).produce_empty_point_df()

config = {
    "share_name": "ODAS",
    "cari_oran_deviation_percentage": 20,
    "df_date": "2023/6"
}

Analyzer(config).initilaze()

