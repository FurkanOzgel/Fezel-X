targetPrice = int(input("How much is your target? "))
budget = int(input("How much is your capital? "))
interestPercentage = int(input("How much base interest percentage? "))

dayCounter = 0

while targetPrice > budget:
    budget = budget + budget * interestPercentage / 100
    dayCounter = dayCounter + 1

print(str(dayCounter) + " Defa tekrarladığınızda hedefinize ulaşabilirsiniz. Yeni bakiyeniz: "+str(budget))