###########################################################
# Allows to calculate payment for differentiated payment.
# Allows to calculate components of annuity payment
# such as: payment, credit principal, payment period.
# Use --help command to see the syntax
###########################################################

import argparse
from math import log, ceil

# Parsing Arguments

parser = argparse.ArgumentParser()

parser.add_argument("--type", "-t", metavar='', help="Give a type of payment you want to calculate",
                    choices=['diff', 'annuity'], action='store')
parser.add_argument("--payment", "-pa", metavar='', help="Give amount of monthly payment",
                    type=int, action='store') # Only for annuity payment
parser.add_argument("--principal", "-pr", metavar='', help="Give amount of credit principal",
                    type=int, action='store') # For both annuity and differentiated
parser.add_argument("--periods", "-pe", metavar='', help="Given number of months and/or years needed to repay the credit",
                    type=int, action='store')
parser.add_argument ("--interest", "-i", metavar='', help="Give amount of interest",
                     type=float, action='store')
args = parser.parse_args()

# Overpayment
def annuity_overpayment_calculator(payment_type, periods, payment, credit_principal):
    if payment_type == 'annuity':
        overpayment = payment - credit_principal
        overpayment = ceil(overpayment)
        print(f'Overpayment = {overpayment}')
    else:
        pass
        
    

## Annuity Derivative calculator ##
def annuity_derivative_calculator(nominal_interest_rate, number_months):
    annuity_derivative = nominal_interest_rate * pow(1 + nominal_interest_rate, number_months) / (pow(1 + nominal_interest_rate, number_months) - 1)
    return annuity_derivative
    
# Nominal interest calculator

def nominal_interest_calculator(credit_interest):
    nominal_interest_rate = credit_interest / (12 * 100)
    return nominal_interest_rate


## Differentiated Payment ##
def differentiated_payment_function(credit_principal, number_months, credit_interest):

    current_period = 1

    def diff_payment_calc(credit_interest, credit_principal, number_months, current_period): # unsure if variables are needed in brackets
        nominal_interest_rate = nominal_interest_calculator(credit_interest)
        differentiated_payment = (credit_principal /
                                  number_months +
                                  nominal_interest_rate *
                                  (credit_principal - (credit_principal * (current_period - 1) / number_months)))
        return ceil(differentiated_payment)

    monthly_payments_list = []
    while current_period <= number_months:
        if current_period < number_months:
            differentiated_payment = diff_payment_calc(credit_interest, credit_principal, number_months, current_period)
            print(f'Month {current_period}: paid out {differentiated_payment}')
            current_period += 1
            monthly_payments_list.append(differentiated_payment)
        elif current_period == number_months:
            differentiated_payment = diff_payment_calc(credit_interest, credit_principal, number_months, current_period)
            print(f'Month {current_period}: paid out {differentiated_payment}')
            monthly_payments_list.append(differentiated_payment)
            break
    overpayment = sum(monthly_payments_list) - credit_principal ## calculating overpayment 
    print(f'\nOverpayment = {overpayment}')

## Annuity payment - periods calculator ##
def periods_calculator(credit_principal, monthly_payment, credit_interest):
    nominal_interest_rate = nominal_interest_calculator(credit_interest)
    number_months = log(monthly_payment / (monthly_payment - nominal_interest_rate * credit_principal), (1 + nominal_interest_rate))
    number_months = ceil(number_months)

    def month_counter_return(credit_principal, monthly_payment, credit_interest):
        months = number_months % 12
        years = int((number_months - months) / 12)
        total_payment = number_months * monthly_payment
        if years == 1 and months == 1:
            print(f'You need {years} year and {months} month to repay this credit!')
            annuity_overpayment_calculator('annuity', number_months, total_payment, args.principal)
        elif years == 1 and months == 0:
            print(f'You need {years} year to repay this credit!')
            annuity_overpayment_calculator('annuity', number_months, total_payment, args.principal)
        elif years == 1:
            print(f'You need {years} year and {months} months to repay this credit!')
            annuity_overpayment_calculator('annuity', number_months, total_payment, args.principal)
        elif months == 1:
            print(f'You need {years} years and {months} month to repay this credit!')
            annuity_overpayment_calculator('annuity', number_months, total_payment, args.principal)
        elif months == 0:
            print(f'You need {years} years to repay this credit!')
            annuity_overpayment_calculator('annuity', number_months, total_payment, args.principal)
        elif months == 1 and years == 0:
            print(f'You need {months} month to repay this credit!')
            annuity_overpayment_calculator('annuity', number_months, total_payment, args.principal)
        elif years == 0:
            print(f'You need {months} months to repay this credit!')
            annuity_overpayment_calculator('annuity', number_months, total_payment, args.principal)
        else:
            print(f'You need {years} years and {months} months to repay this credit!')
            annuity_overpayment_calculator('annuity', number_months, total_payment, args.principal)

    return month_counter_return(args.principal, args.payment, args.interest)


## Annuity payment - payment calculator ##
def annuity_payment_calculator(credit_principal, number_months, credit_interest):
    nominal_interest_rate = nominal_interest_calculator(args.interest)
    annuity_derivative = annuity_derivative_calculator(nominal_interest_rate, args.periods)
    annuity_payment = credit_principal * annuity_derivative
    print(f'Your annuity payment = {ceil(annuity_payment)}!')
    annuity_payment = ceil(annuity_payment) * number_months
    annuity_overpayment_calculator('annuity', args.periods, annuity_payment, credit_principal)


## Annuity Payment - principal calculator ##
def credit_principal_calculator(monthly_payment, number_months, credit_interest):
    nominal_interest_rate = nominal_interest_calculator(args.interest)
    annuity_derivative = annuity_derivative_calculator(nominal_interest_rate, number_months)
    credit_principal = monthly_payment / annuity_derivative
    credit_principal = round(credit_principal)
    print(f'Your credit principal = {credit_principal}!')
    total_payment = number_months * monthly_payment
    annuity_overpayment_calculator('annuity', args.periods, total_payment, credit_principal)

## Main function ##
def main():
    if args.type == 'annuity':
        if args.payment == None and (args.principal and args.periods and args.interest) != None:
            annuity_payment_calculator(args.principal, args.periods, args.interest)
        elif args.principal == None and (args.payment and args.periods and args.interest) != None:
            credit_principal_calculator(args.payment, args.periods, args.interest)
        elif args.periods == None and (args.principal and args.payment and args.interest) != None:
            periods_calculator(args.principal, args.payment, args.interest)
        else:
            print("Incorrect parameters")
    elif args.type == 'diff':
        if (args.principal and args.periods and args.interest) != None and args.payment == None:
            differentiated_payment_function(args.principal, args.periods, args.interest)
        else:
            print("Incorrect parameters")
        
    
if __name__ == '__main__':
    main()
