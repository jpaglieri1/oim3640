

product = 100 #in $s
tax_rate = 0.0625
tax1 = product * tax_rate
print(f'The tax on a product that costs ${product} is {tax1}')

computer_price = 900
iphone_price = 1100

def calc_tax(price):
    """Calculate produce tax based on given price"""
    tax_rate = 0.0625
    tax = price*tax_rate
    #print(f"The tax for a product which costs ${price} us {tax}")
    #print(tax)
    #if the function does not explicitly return any value, it would return None
    return tax

tax_computer = calc_tax(computer_price)
tax_iphone = calc_tax(computer_price)

total_tax = tax_computer + tax_iphone
print(total_tax)