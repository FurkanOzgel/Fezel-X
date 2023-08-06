
'''
Cari oran, bir şirketin kısa vadeli borçlarını ödeyebilme yeteneğini ölçen bir finansal orandır. 
Bu oran, şirketin mevcut varlıklarının, kısa vadeli borçlarının ne kadarını karşılayabileceğini gösterir.

1- Cari oranın ideal seviyesi 2'dir.

2- Cari oranda sektör ortalaması bulunmalı. Cari oran sektör ortalamasının altındaysa bu şirketin kısa vadede borçlarını 
ödeme zorluğu çekebileceğini gösterir ama ortalamanın üstündeyse bu şirketin finansal durumunun diğer şirketlerden daha 
iyi olduğunu gösterebilir.

3-  Şirketin cari oranı, zaman içinde değişebilir. Bu nedenle, şirketin cari oranının trendini takip etmek önemlidir.
Cari oranın düşmesi, şirketin kısa vadeli borçlarını ödeyememe riskini artırabilir. Öte yandan, cari oranın yükselmesi,
şirketin finansal durumunun iyileştiğine işaret edebilir.

'''

import json

with open("Bist_R&D/Basic_Analysis/Analyzer/BlanceSheet.json", "r") as file:
    ratios = json.loads(file.readline())

print(ratios["Cari_Oran"])