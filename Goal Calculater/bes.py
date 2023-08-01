payment = float(input("Enter your monthly payment amount: "))
interest = float(input("Enter your monthly interest amount: ")) / 100
state_interest = float(input("Enter your monthly state interest amount: ")) / 100
month_count = int(input("Enter month count: "))
percent_state = int(input("Enter percent state benefit: ")) /100

total_own_balance = 0
total_state_balance = 0

for i in range(month_count+1)[1:]:

    if i%11 == 0 or i%12 == 0:
        total_own_balance = total_own_balance + total_own_balance * interest
    else:
        total_own_balance = total_own_balance + payment + (total_own_balance + payment) * interest

    total_state_balance = total_state_balance + payment * 0.3 + (total_state_balance + payment * 0.3) * state_interest

print(" ")
print(" ")
print("Toplam yatırılan tutar: "+str(int(month_count*payment))+" TL")
print(" ")
print("Devlet katkısı hariç toplam bakiyeniz: "+ str(int(total_own_balance))+" TL")
print(" ")
print(f"Toplam devlet katkısı: {int(total_state_balance)} TL , hak edilen devlet katkısı: {int(total_state_balance * percent_state)} TL")
print(" ")
print(f"Toplam alınacak para: {int(total_own_balance + total_state_balance * percent_state)} TL\n\n"
      f"Toplam kâr: %{int((int((total_own_balance + total_state_balance * percent_state)-(month_count*payment)) * 100) / int(month_count*payment))}\
  ({int((total_own_balance + total_state_balance * percent_state)-(month_count*payment))} TL)")
print(" ")
