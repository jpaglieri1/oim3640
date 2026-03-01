#Here is my prototype for mini project 1
import math
import pandas as pd

def opening():
    """This will be what displays at the beginning of the program."""
    print("\n1. Calculator")
    print("2. Amortization Table")
    print("3. Input new data")
    print("4. Exit")
    progopt = input("Select an option by inputting it's corresponding number: ")
    return(progopt)

def calculator(pv, intrate, payment, fv, pers):
    """The user will be able to calculate present value, future value, interest, and payment, and term."""
    if fv == 0.0:
        calcfv = (pv*((1+intrate)**pers))+(payment*((((1+intrate)**pers)-1)/intrate))
    elif pv == 0.0:
        calcpv = (fv/(1+(intrate**pers)))
    elif payment == 0.0:
        calcpay = ((pv*intrate))/(1-((1+intrate)**(-pers)))
    elif intrate == 0.0:
        calcint = ((fv/pv)**(1/pers))-1
    else:
        calcper = (math.log(fv/pv))/(math.log(1+intrate))
     
    print(f"\nPrincipal = {pv}")
    print(f"Interest Rate = {calcint}%")
    print(f"Payment Amount = {payment}")
    print(f"Future Value = {calcfv}")
    print(f"Number of periods = {pers}")
    input("\nPress enter to return to main menu")

def amortization(pv, intrate, payment, fv, pers):
    """The program will develop an amoritiztion table for the user to view based on their inputted data"""
    princamt = 0
    intamt = 0
    endbal = pv
    begbal_list = []
    payval_list = []
    princamt_list = []
    intamt_list = []
    endbal_list = []
    
    for i in (range(pers+1)):
        begbal_list.append(endbal)
        payval_list.append(payment)
        intamt = endbal*(intrate)
        princamt = payment - intamt
        princamt_list.append(princamt)
        intamt_list.append(intamt)
        endbal = endbal - princamt
        endbal_list.append(endbal)

    df = pd.DataFrame({
        "Beginning balance": begbal_list,
        "Payment": payval_list,
        "Principal": princamt_list,
        "Interest": intamt_list, 
        "Ending Balance": endbal_list
        })
    print(df)

    input("Press enter to return to main menu")

run = 0

#Main Code
pv = float(input("Insert the principal amount or enter 0: "))
fv = float(input("Insert the future value of the loan or enter 0: "))
intrate = float(input("Insert the interest rate (as a decimal) or enter 0: "))
payment = float(input("Insert the payment or enter 0: "))
pers = float(input("Input the length of the loan/investment or enter 0: "))
amtcomp = float(input("Insert the number of times compounded in a year: "))
pers = int(pers*amtcomp)
intrate = intrate/amtcomp
while run != 1:
    choice = opening()
    if choice == "1":
        calculator(pv, intrate, payment, fv, pers)
    elif choice == "2":
        amortization(pv, intrate, payment, fv, pers)
    elif choice == "3":
        pv = float(input("Insert the pricipal amount or enter 0: "))
        fv = float(input("Insert the future value of the loan or enter 0: "))
        intrate = float(input("Insert the interest rate (as a decimal) or enter 0: "))
        payment = float(input("Insert the payment or enter 0: "))
        pers = float(input("Input the length of the loan/investment or enter 0: "))
        amtcomp = float(input("Insert the number of times compounded in a year: "))
        pers = int(pers*amtcomp)
        intrate = intrate/amtcomp
    elif choice == "4":
        run = 1
    else:
        print("Invalid input")