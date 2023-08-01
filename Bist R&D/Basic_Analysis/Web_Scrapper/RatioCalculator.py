import BalanceSheet

def calculate_ratios(stock):

    BalanceSheet.run_driver()
    
    global bilanco_df

    ratio_json = {}
    bilanco_date = BalanceSheet.get_finance_data_dates(stock)[0].split("/")
    bilanco_df = BalanceSheet.get_financal_tables(stock, bilanco_date[0],
                                                  bilanco_date[1])

    last_year = BalanceSheet.get_finance_data_dates(stock)[4].split("/")
    last_year_df = BalanceSheet.get_financal_tables(stock, last_year[0],
                                                    last_year[1])

    cari_oran = 0
    nakit_oran = 0
    kisa_vadeli_borc_oranı = 0
    uzun_vadeli_borc_oranı = 0
    yabancı_ve_oz_kaynak_oranı = 0
    alacak_devir_hızı = 0
    alacakların_ortalama_tahsil_süresi = 0
    aktif_devir_hızı = 0
    donem_karı_oz_kaynaklar_oranı = 0
    stok_devir_hızı = 0
    pd_dd_oranı = BalanceSheet.get_ready_ratio(stock, '//*[@id="ctl00_ctl58_g_e55f617d_8944_4235_a4a3_cb95ded58989"]/div/div/div[2]/div/div/table/tbody/tr/td[6]')
    ozkaynak_karlılıgı = BalanceSheet.get_ready_ratio_tradingview(f"BIST-{stock}", "/html/body/div[3]/div[4]/div[2]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[13]/div[5]/div[8]/div/div")
    varlık_getirisi = BalanceSheet.get_ready_ratio_tradingview(f"BIST-{stock}", "//*[@id='js-category-content']/div[2]/div/div/div[6]/div[2]/div/div[1]/div[12]/div[5]/div[8]/div/div")
    özkakynak_karlılıgı = BalanceSheet.get_ready_ratio_tradingview(f"BIST-{stock}", "//*[@id='js-category-content']/div[2]/div/div/div[6]/div[2]/div/div[1]/div[13]/div[5]/div[8]/div/div")
    yatırılan_sermayenin_getirisi = BalanceSheet.get_ready_ratio_tradingview(f"BIST-{stock}", '//*[@id="js-category-content"]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[14]/div[5]/div[8]/div/div')
    brüt_kar_marjı = BalanceSheet.get_ready_ratio_tradingview(f"BIST-{stock}", '//*[@id="js-category-content"]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[15]/div[5]/div[8]/div/div')
    faaliyet_kar_marjı = BalanceSheet.get_ready_ratio_tradingview(f"BIST-{stock}", '//*[@id="js-category-content"]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[16]/div[5]/div[8]/div/div')
    favök_marjı = BalanceSheet.get_ready_ratio_tradingview(f"BIST-{stock}", '//*[@id="js-category-content"]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[17]/div[5]/div[8]/div/div')
    net_marj = BalanceSheet.get_ready_ratio_tradingview(f"BIST-{stock}", '//*[@id="js-category-content"]/div[2]/div/div/div[6]/div[2]/div/div[1]/div[17]/div[5]/div[8]/div/div')
    hbk = BalanceSheet.get_ready_ratio_tradingview_summary(f"BIST-{stock}", "//*[@id='js-category-content']/div[2]/div/section/div[2]/div[2]/div[4]/div[2]/div[1]")
    fiyat_kazanc = BalanceSheet.get_ready_ratio_tradingview_summary(f"BIST-{stock}", "//*[@id='js-category-content']/div[2]/div/section/div[2]/div[2]/div[3]/div[2]/div[1]")



    kisa_vadeli_yabanci_kaynaklar = 0
    uzun_vadeli_yabanci_kaynaklar = 0
    tum_donen_varlıklar = 0
    nakit_nakit_benzeri = 0
    finansal_yatırımlar = 0
    pasif_toplam = 0
    oz_kaynaklar = 0
    ticari_alacaklar_ortalamasi = 0
    sales_ortalamasi = 0
    alacak_ortalamasi = 0
    sales = 0 
    alacaklar = 0 
    diger_alacaklar = 0
    toplam_varlıklar = 0
    donem_karı = 0
    satis_maliyeti = 0
    stok = 0
    ortalama_stok = 0
    ortalama_borclar = 0
    
    for i, row in bilanco_df.iterrows():
        if row.ItemCode == "2A":
            kisa_vadeli_yabanci_kaynaklar = float(row.Values)

        elif row.ItemCode == "1AI":
            tum_donen_varlıklar = tum_donen_varlıklar + float(row.Values)

        elif row.ItemCode == "1AA":
            nakit_nakit_benzeri = float(row.Values)

        elif row.ItemCode == "1AB":
            finansal_yatırımlar = float(row.Values)

        elif row.ItemCode == "2ODB":
            pasif_toplam = float(row.Values)

        elif row.ItemCode == "2B":
            uzun_vadeli_yabanci_kaynaklar = float(row.Values)

        elif row.ItemCode == "2N":
            oz_kaynaklar = float(row.Values)

        elif row.ItemCode == "3C":

            sales = float(row.Values) 

            for i, y in last_year_df.iterrows():
                if y.ItemCode == "3C":
                    last_year_sales = float(y.Values)
            sales_ortalamasi = (float(row.Values) + last_year_sales) / 2

        elif row.ItemCode == "1AC":

            alacaklar = float(row.Values)

            for i, y in last_year_df.iterrows():
                if y.ItemCode == "1AC":
                    last_year_alacak = float(y.Values)

            alacak_ortalamasi = (float(row.Values) + last_year_alacak) / 2
            
        elif row.ItemCode == "1AE":
            diger_alacaklar = float(row.Values)
        
        elif row.ItemCode == "1BL":
            toplam_varlıklar = float(row.Values)

        elif row.ItemCode == "3L":
            donem_karı = float(row.Values)

        elif row.ItemCode == "3CA":
            satis_maliyeti = float(row.Values) * -1

        elif row.ItemCode == "1AF":

            stok = float(row.Values)

            for i, y in last_year_df.iterrows():
                if y.ItemCode == "1AF":
                    last_year_stok = float(y.Values)

            ortalama_stok = (float(row.Values) + last_year_stok) / 2
            
    cari_oran = tum_donen_varlıklar / kisa_vadeli_yabanci_kaynaklar
    ratio_json["Cari_Oran"] = cari_oran

    nakit_oran = (nakit_nakit_benzeri + finansal_yatırımlar) / kisa_vadeli_yabanci_kaynaklar
    ratio_json["Nakit_Oran"] = nakit_oran

    kisa_vadeli_borc_oranı = kisa_vadeli_yabanci_kaynaklar / pasif_toplam
    ratio_json["Kısa_Vadeli_Borç_Oranı"] = kisa_vadeli_borc_oranı

    uzun_vadeli_borc_oranı = uzun_vadeli_yabanci_kaynaklar / pasif_toplam
    ratio_json["Uzun_Vadeli_Borç_Oranı"] = uzun_vadeli_borc_oranı

    yabancı_ve_oz_kaynak_oranı = (uzun_vadeli_yabanci_kaynaklar + kisa_vadeli_yabanci_kaynaklar) / oz_kaynaklar
    ratio_json["Yabancı_Kaynakların_Öz_Kaynaklara_Oranı"] = yabancı_ve_oz_kaynak_oranı

    alacak_devir_hızı = sales_ortalamasi / alacak_ortalamasi
    ratio_json["Alacak_Devir_Hızı"] = alacak_devir_hızı

    alacakların_ortalama_tahsil_süresi = 365 * (alacaklar + diger_alacaklar) / sales
    ratio_json["Alacak_Ortalama_Tahsil_Süresi"] = alacakların_ortalama_tahsil_süresi

    aktif_devir_hızı = sales/toplam_varlıklar
    ratio_json["Aktif_Devir_Hızı"] = aktif_devir_hızı

    donem_karı_oz_kaynaklar_oranı = donem_karı / oz_kaynaklar
    ratio_json["Dönem_Kârı/Öz_Kaynaklar"] = donem_karı_oz_kaynaklar_oranı

    stok_devir_hızı = satis_maliyeti / ortalama_stok
    ratio_json["Stok_Devir_Hızı"] = stok_devir_hızı

    ratio_json["PD/DD"] = pd_dd_oranı

    ratio_json["Özkaynak_Karlılığı"] = ozkaynak_karlılıgı

    ratio_json["Varlık_Getirisi_%"] = varlık_getirisi 
    ratio_json["Özkaynak_Karlılığı_%"] = özkakynak_karlılıgı  
    ratio_json["Yatrılan_Sermayenin_Getirisi_%"] = yatırılan_sermayenin_getirisi  
    ratio_json["Brüt_Kar_Marjı_%"] = brüt_kar_marjı  
    ratio_json["Faaliyet_Kar_Marjı_%"] = faaliyet_kar_marjı  
    ratio_json["Favök_Marjı_%"] = favök_marjı  
    ratio_json["Net_Marj_%"] = net_marj 

    ratio_json["Hisse_Başı_Kazanç"] = hbk

    ratio_json["Fiyat_Kazanç_Oranı"] = fiyat_kazanc

    return ratio_json

# BalanceSheet.run_driver()

# data_object = calculate_ratios("PENTA")

# for i in data_object.keys():

#     print(i+": "+str(round(data_object[i], 2)))