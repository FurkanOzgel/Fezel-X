import ratioDf
from analyzer import Analyzer
import modelTest

# ratioDf.create_share_ratio_df()
# ratioDf.update_share_ratio_df()
# ratioDf.create_share_sector_df()
# ratioDf.update_share_sector_df()
# ratioDf.produce_sector_average_df()

# ratioDf.create_share_ratio_df("2023/6")
# ratioDf.create_share_ratio_df("2023/3")
# ratioDf.create_share_ratio_df("2022/12")

# ratioDf.produce_sector_average_df("2022/12")
# ratioDf.produce_sector_average_df("2023/3")
# ratioDf.produce_sector_average_df("2023/6")

# analyzer.produce_empty_point_df("2022/12")
# analyzer.produce_empty_point_df("2023/3")
# analyzer.produce_empty_point_df("2023/6")

# ratioDf.get_price_increase_percentages("2022/12")
# ratioDf.get_price_increase_percentages("2023/3")

config = {
    "share_name": "ODAS",
    "cari_oran_deviation_percentage": 30,
    "cari_oran_percentage_change_for_the_trend": 0.19,
    "df_date": "2023/3",
    "cari_oran_rating": [5, 2, 3, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    "nakit_oran_rating": [1, 1, 1],
    "yabancı_kaynak_ozkaynak_rating": [1, 1, 1, 1]
}

Analyzer(config).initilaze()

# modelTest.fill_point_df("2022/12")