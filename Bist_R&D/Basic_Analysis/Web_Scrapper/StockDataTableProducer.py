import pandas as pd
from RatioCalculator import Stock
import BalanceSheet

stock_list = pd.read_csv("Bist_R&D/Basic_Analysis/StockList.csv", index_col=0)

columns = ["Stock_Name", "Bilanco_Date", "Cari_Oran", "Nakit_Oran", "Toplam_Yabancı_Kaynaklar_Oz_Kaynaklar_Oranı", "Alacak_Devir_Hızı",
           "Aktif_Devir_Hızı", "Oz_Varlık_Karlılıgı", "Kar_Marjları", "Hisse_Bası_Kazanc", "Fiyat_Satıs_Oranı"]


try:
    stock_data_list = pd.read_csv("Bist_R&D/Basic_Analysis/StockDataList.csv", index_col=0)
except:
    stock_data_list = pd.DataFrame(columns=columns)

for index, row in stock_list.iterrows():
    try:
        if("," in row["Stock"]):
            raise("Invalid stock")
        
        stock = Stock(row["Stock"])
        
        stock_name = stock.stockName
        bilanco_date = stock.sheetDate[0] + "/" +stock.sheetDate[1]
        cari_oran = stock.cariOran()
        nakit_oran = stock.nakitOran()
        toplam_yabancı_kaynaklar_oz_kaynaklar = stock.toplamYabancıKaynaklarOzKaynaklar()
        alacak_devir_hızı = stock.alacakDevirHızı()
        aktif_devir_hızı = stock.aktifDevirHızı()
        oz_varlık_karlılıgı = stock.ozvarlıkKarlılıgı()
        kar_marjları = stock.karMarjları()
        hisse_bası_kazanc = stock.hisseBasıKazanc()
        fiyat_satıs_oranı = stock.fiyatSatısOranı()
        
        BalanceSheet.stop_driver()

        new_row = {
                   "Stock_Name": stock_name, "Bilanco_Date": bilanco_date, "Cari_Oran": cari_oran,
                   "Nakit_Oran": nakit_oran, "Toplam_Yabancı_Kaynaklar_Oz_Kaynaklar_Oranı": toplam_yabancı_kaynaklar_oz_kaynaklar,
                   "Alacak_Devir_Hızı": alacak_devir_hızı, "Aktif_Devir_Hızı": aktif_devir_hızı,
                   "Oz_Varlık_Karlılıgı": oz_varlık_karlılıgı, "Kar_Marjları": kar_marjları, 
                   "Hisse_Bası_Kazanc": hisse_bası_kazanc, "Fiyat_Satıs_Oranı": fiyat_satıs_oranı
                   }
        
        stock_data_list.loc[len(stock_data_list)] = new_row 
        
        print(f"{stock.stockName} Scarapping Done")
        
    except Exception as a:
        with open("Bist_R&D/Basic_Analysis/lastItem.txt", "a", encoding="UTF-8") as file:
            file.write(stock.stockName + "\n")

stock_data_list.to_csv("Bist_R&D/Basic_Analysis/StockDataList.csv")