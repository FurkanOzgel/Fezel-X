import pandas as pd



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