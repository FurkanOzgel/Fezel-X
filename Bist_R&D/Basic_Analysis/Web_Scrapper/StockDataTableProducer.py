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
    
with open("Bist_R&D/Basic_Analysis/faulty_stocks.txt", "r", encoding="UTF-8") as file:
    mistake_count = len(file.readlines()) - 1
    
    if mistake_count == -1:
        mistake_count = 0
    
start_index = stock_data_list.shape[0] + mistake_count

BalanceSheet.run_driver()

for index, row in stock_list[start_index:].iterrows():
    
    with open("Bist_R&D/Basic_Analysis/loop_stopper.txt", "r", encoding="UTF-8") as file:
        runLoop = file.read()
            
    try:
        if runLoop == "0":
            raise Exception("You Stopped Loop")
        
        if("," in row["Stock"]):
            raise Exception("Invalid stock")
        
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

        new_row = {
                   "Stock_Name": stock_name, "Bilanco_Date": bilanco_date, "Cari_Oran": cari_oran,
                   "Nakit_Oran": nakit_oran, "Toplam_Yabancı_Kaynaklar_Oz_Kaynaklar_Oranı": toplam_yabancı_kaynaklar_oz_kaynaklar,
                   "Alacak_Devir_Hızı": alacak_devir_hızı, "Aktif_Devir_Hızı": aktif_devir_hızı,
                   "Oz_Varlık_Karlılıgı": oz_varlık_karlılıgı, "Kar_Marjları": kar_marjları, 
                   "Hisse_Bası_Kazanc": hisse_bası_kazanc, "Fiyat_Satıs_Oranı": fiyat_satıs_oranı
                   }
        
        stock_data_list.loc[len(stock_data_list)] = new_row 

        stock_data_list.to_csv("Bist_R&D/Basic_Analysis/StockDataList.csv")
        
        print(f"{stock.stockName} Scarapping Done")
        
    except Exception as e:
        print(e)

        if runLoop == "0":
            break
        else:
            with open("Bist_R&D/Basic_Analysis/faulty_stocks.txt", "a", encoding="UTF-8") as file:
                file.write(row["Stock"] + "\n")

BalanceSheet.stop_driver()

stock_data_list.to_csv("Bist_R&D/Basic_Analysis/StockDataList.csv")