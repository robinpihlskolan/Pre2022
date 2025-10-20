interest_yearly = 4.75/100 #percent yearly
interest_monthly = interest_yearly/12 #percent monthly

total_payback_monthly = 10000 #monthly total pay

loan = 1200000  #loan

months = 0
while loan >= 0:
    interest_now = loan*interest_monthly
    amortization = total_payback_monthly - interest_now #10000-interest_now=amortization
    print(amortization)
    loan = loan - amortization
    months = months + 1

print(months/12)


