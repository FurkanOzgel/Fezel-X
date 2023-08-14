# encoding:utf-8

import BalanceSheet
import numpy as np

class Stock:
    def __init__(self, stockName):

        self.stockName = stockName
        
        self.sheetDate = BalanceSheet.get_finance_data_dates(stockName)[0].split("/")

        last_year = BalanceSheet.get_finance_data_dates(stockName)[4].split("/")
        self.last_year_sheet = BalanceSheet.get_financal_tables(stockName, last_year[0],
                                                        last_year[1])
        
        self.sheet = BalanceSheet.get_financal_tables(stockName, self.sheetDate[0], self.sheetDate[1])
        self.historicalSheet = BalanceSheet.get_historical_financal_tables(stockName)
        
        
    def cariOran(self):
        tum_donen_varlıklar = np.array(self.historicalSheet[self.historicalSheet["ItemCode"] == '1AI'].iloc[0, 1:].tolist(), dtype=float)
        kisa_vadeli_yabanci_kaynaklar = np.array(self.historicalSheet[self.historicalSheet["ItemCode"] == '2A'].iloc[0, 1:].tolist(), dtype=float)

        return (tum_donen_varlıklar / kisa_vadeli_yabanci_kaynaklar)
    
    def nakitOran(self):
        nakit_nakit_benzeri = np.array(self.historicalSheet[self.historicalSheet["ItemCode"] == '1AA'].iloc[0, 1:].tolist(), dtype=float)
        finansal_yatırımlar = np.array(self.historicalSheet[self.historicalSheet["ItemCode"] == '1AB'].iloc[0, 1:].tolist(), dtype=float)
        kisa_vadeli_yabanci_kaynaklar = np.array(self.historicalSheet[self.historicalSheet["ItemCode"] == '2A'].iloc[0, 1:].tolist(), dtype=float)
        
        return (nakit_nakit_benzeri + finansal_yatırımlar) / kisa_vadeli_yabanci_kaynaklar
    
    def toplamYabancıKaynaklarOzKaynaklar(self):
        uzun_vadeli_yabanci_kaynaklar = np.array(self.historicalSheet[self.historicalSheet["ItemCode"] == '2B'].iloc[0, 1:].tolist(), dtype=float)
        kisa_vadeli_yabanci_kaynaklar = np.array(self.historicalSheet[self.historicalSheet["ItemCode"] == '2A'].iloc[0, 1:].tolist(), dtype=float)
        oz_kaynaklar = np.array(self.historicalSheet[self.historicalSheet["ItemCode"] == '2N'].iloc[0, 1:].tolist(), dtype=float)
        
        return (uzun_vadeli_yabanci_kaynaklar + kisa_vadeli_yabanci_kaynaklar) / oz_kaynaklar
    
    def alacakDevirHızı(self):
        sales = float(self.sheet[self.sheet["ItemCode"] == '3C'].iloc[0, 1])

        for i, y in self.last_year_sheet.iterrows():
            if y.ItemCode == "3C":
                last_year_sales = float(y.Values)
        sales_ortalamasi = (float(sales) + last_year_sales) / 2
        
        alacaklar = float(self.sheet[self.sheet["ItemCode"] == '1AC'].iloc[0, 1])

        for i, y in self.last_year_sheet.iterrows():
            if y.ItemCode == "1AC":
                last_year_alacak = float(y.Values)
                
        alacak_ortalamasi = (alacaklar + last_year_alacak) / 2
        
        return sales_ortalamasi / alacak_ortalamasi
    
    def aktifDevirHızı(self):
        sales = float(self.sheet[self.sheet["ItemCode"] == '3C'].iloc[0, 1])
        toplam_varlıklar = float(self.sheet[self.sheet["ItemCode"] == '1BL'].iloc[0, 1])
        
        return sales/toplam_varlıklar
    
    def karMarjları(self):        
        varlık_getirisi = BalanceSheet.get_ready_historical_ratio_tradingview("//*[@id='js-category-content']/div[2]/div/div/div[6]/div[2]/div/div[1]/div[12]/div[5]")
        yatırılan_sermayenin_getirisi = BalanceSheet.get_ready_historical_ratio_tradingview('//*[@id="js-category-content"]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[14]/div[5]')
        brüt_kar_marjı = BalanceSheet.get_ready_historical_ratio_tradingview('//*[@id="js-category-content"]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[15]/div[5]')
        faliyet_kar_marjı = BalanceSheet.get_ready_historical_ratio_tradingview('//*[@id="js-category-content"]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[16]/div[5]')
        favök_marjı = BalanceSheet.get_ready_historical_ratio_tradingview('//*[@id="js-category-content"]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[17]/div[5]')
        net_marj = BalanceSheet.get_ready_historical_ratio_tradingview('//*[@id="js-category-content"]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[18]/div[5]')
        
        return {
            "varlık_getirisi": varlık_getirisi,
            "yatırılan_sermayenin_getirisi": yatırılan_sermayenin_getirisi, 
            "brüt_kar_marjı": brüt_kar_marjı, 
            "faliyet_kar_marjı": faliyet_kar_marjı, 
            "favök_marjı": favök_marjı, 
            "net_marj": net_marj
            }
    
    def ozvarlıkKarlılıgı(self):
        BalanceSheet.set_driver_for_historical(self.stockName)
        
        return BalanceSheet.get_ready_historical_ratio_tradingview( "//*[@id='js-category-content']/div[2]/div/div/div[6]/div[2]/div/div[1]/div[13]/div[5]")
    
    def hisseBasıKazanc(self):
        return BalanceSheet.get_historical_hbk(self.stockName)
    
    def fiyatSatısOranı(self):
        fiyat_kazanc = BalanceSheet.get_ready_ratio_tradingview_summary(f"BIST-{self.stockName}", "//*[@id='js-category-content']/div[2]/div/section/div[2]/div[2]/div[3]/div[2]/div[1]")
        
        return fiyat_kazanc
