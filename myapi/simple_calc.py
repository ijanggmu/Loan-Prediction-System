# program shows the details of the loan

# will take the input values from user

principal = float(input("total loan amount taken: "))
interest_rate = float(input("annual interest rate applied: "))
duration = int(input("loan duration in years: "))

# ---function for monthly loan amount calculation---
def monthly_loan(principal,interest_rate,duration):
    n = duration*12 #total number of months
    r = interest_rate/(100*12) #interest per month
    monthly_payment = principal*((r*((r+1)**n))/(((r+1)**n)-1)) #formula for compound interest applied on mothly payments.
    return monthly_payment

# ---funtion for remaining loan balance calculation---
def remaining_bal(principal,annual_interest_rate,duration,payments):
    r = annual_interest_rate/1200 # monthly interest rate
    m = r + 1
    n = duration*12 # duration in months
    
    # remaining balance using compound interest formula
    remaining = principal*(((m**n)-(m**payments))/((m**n)-1))
    return remaining

monthly = monthly_loan(principal,interest_rate,duration)

print("\n\nLoan amount: ",principal," Interest rate: ",interest_rate)

print("\nDuration (Years): ",duration," Monthly payment: ",int(monthly),"\n")

for x in range(1,duration+1):
    mon = x*12
    rem = remaining_bal(principal,interest_rate,duration,mon)
    print("Year: ",x," Balance remaining: ",int(rem)," Total payments: ",int(monthly*mon))