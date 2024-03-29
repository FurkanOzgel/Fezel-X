'''
Cari oran, bir şirketin kısa vadeli borçlarını ödeyebilme yeteneğini ölçen bir finansal orandır. 
Bu oran, şirketin mevcut varlıklarının, kısa vadeli borçlarının ne kadarını karşılayabileceğini gösterir.

1-) Cari oranın ideal seviyesi 1.5 - 2 aralığıdır. (min değerine baktım)

1-) 1 den büyük mü?
2-) 1.5 - 2 aralığına çok uzak değilse bu aralıkta olup olmamasına dikkat et.


2-) Cari oranda sektör ortalaması bulunmalı. Cari oran sektör ortalamasının altındaysa bu şirketin kısa vadede borçlarını 
ödeme zorluğu çekebileceğini gösterir ama ortalamanın üstündeyse bu şirketin finansal durumunun diğer şirketlerden daha 
iyi olduğunu gösterebilir.

3-)  Şirketin cari oranı, zaman içinde değişebilir. Bu nedenle, şirketin cari oranının trendini takip etmek önemlidir.
Cari oranın düşmesi, şirketin kısa vadeli borçlarını ödeyememe riskini artırabilir. Öte yandan, cari oranın yükselmesi,
şirketin finansal durumunun iyileştiğine işaret edebilir.

3.1-) Trend tespit edilmeli (Bizim için trend nedir ?)
3.2-) Son oran trend doğrultusundaysa nötr (Ufak hareketler tred kırılımı sayılmamalıs)
      Trendden farklı ama yararlıysa up 
      Trendden farklı ama zararlıysa down
'''

import json

def analyseCariOran(shareName):

    with open("Bist_R&D/Basic_Analysis/Analyzer/RatioSheet.json", "r") as file:
        ratios = json.loads(file.readline())

    print(ratios["Cari_Oran"])
    
analyseCariOran()