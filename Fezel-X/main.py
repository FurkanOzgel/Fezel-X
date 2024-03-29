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
    "cari_oran_deviation_percentage": 30,
    "devir_hızı_deviation_percentage": 0.1,
    "oz_varlık_deviation_percentage": 0.1,
    "kar_marjları_deviation_percentage": 0.1,
    "fs_deviation_percentage": 0.1,
    "cari_oran_percentage_change_for_the_trend": 0.19,
    "cari_oran_rating": [6, 2, 3, 5, 5, 5, 12, 5, 5, 5, 5, 5],
    "nakit_oran_rating": [1, 1, 1],
    "yabancı_kaynak_ozkaynak_rating": [1, 1, 1, 1],
    "alacak_devir_hızı_rating": [4, 5, 2],
    "aktif_devir_hızı_rating": [4, 5, 7],
    "ozvarlık_karlıgı_rating": [4, 5, 2, 2, 1],
    "kar_marjları_rating": [1, 2, 5, 4, 5],
    "hbk_rating": [1, 2],
    "fs_rating": [1, 2, 2]
}

# Analyzer(config).initilaze()

# modelTest.run_test("2023/3", config)

modelTest.search_config_value("2023/3")

# modelTest.fill_point_df("2022/12")