import pandas as pd

import re
from datetime import datetime


'''**** Bilanco Date Excell Process to Csv ****'''
# import os
# def duzenle_tarih(tarih):
#     tarih = str(tarih)
#     if '/' in tarih:
#         return tarih.split('/')[0]
#     return tarih
# date = "2023-6"
# df = pd.read_excel(f"report_date/{date}.xlsx", index_col=0)
# df.index.name = 'Index'
# col_list = df.iloc[0].to_list()
# df.columns = col_list
# df = df[1:]
# df = df[['Kod\n(BIAS Code)', 'Finansal Tablo\n(Financial Statement)']].dropna()
# df.columns = ["Share", "Report_Date"]
# df['Report_Date'] = df['Report_Date'].apply(duzenle_tarih)
# df.to_csv(f"report_date/{date}.csv")
# os.remove(f"report_date/{date}.xlsx")

'''**** Bilanco Date Excell Fix Date ****'''

def is_valid_date_format(date_str):
    # Tarih ifadesini doğru formatta kontrol etmek için bir regex kullanabiliriz.
    # Bu regex, "YYYY-MM-DD HH:MM:SS" formatındaki tarih ifadesini kontrol eder.
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
    
    # Verilen tarih ifadesini regex ile karşılaştırın.
    if date_pattern.match(date_str):
        return True
    else:
        return False

def convert_date_format(date_str):
    try:
        # Verilen tarih ifadesini "DD.MM.YYYY" formatında ayrıştırın.
        parts = date_str.split('.')
        day = parts[0].strip()
        month = parts[1].strip()
        year = parts[2].strip()
        
        # Tek haneli gün ve ay değerlerini iki haneli olarak biçimlendirin.
        day = day.zfill(2)
        month = month.zfill(2)
        
        # Tarihi hedef formata dönüştürün.
        new_date_str = f"{year}-{month}-{day} 00:00:00"
        
        return new_date_str
    except (ValueError, IndexError):
        return None 


date = "2023-6"
df = pd.read_csv(f"data/report_date/{date}.csv", index_col=0)

for index, row in df.iterrows():
    if is_valid_date_format(row["Report_Date"]):
        pass
    else:
        df.at[index, "Report_Date"] = convert_date_format(row["Report_Date"])

df.to_csv(f"data/report_date/{date}.csv")