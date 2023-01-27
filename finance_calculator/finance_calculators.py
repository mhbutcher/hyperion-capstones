# First Capstone project - Finance Calculators
import math

# Display the choice menu to the user, Investment or Bonds

print("Choose either 'Investment' or 'Bond' from the menu below to proceed:")
print(
    "Investment - to calculate the amount of interest you'll earn on your investment\nBond - to calculate the amount "
    "you'll have to pay on a home loan"
)
which_calc = input("\nSelection: ")
# Set any response to lowercase, will pass the if statements next
which_calc.lower()

if which_calc == "investment":
    # Get all the questions out of the way in one go. Change interest to lowercase so it passes into if statements
    deposit = float(input("Deposit value: $"))
    interest_rate = float(input("Interest rate (%): "))
    timeline = int(input("Length of investment (years): "))
    interest = str(input("Simple or Compound interest: "))
    interest.lower()

    # Calculations for the interest choices
    new_interest_rate = interest_rate / 100
    if interest == "simple":
        total_investment = round(deposit * (1 + new_interest_rate * timeline), 2)
    elif interest == "compound":
        total_investment = round(
            deposit * math.pow((1 + new_interest_rate), timeline), 2
        )

    # Error catching to prevent printing the result line if something was typed incorrectly
    if interest != "simple" or interest != "compound":
        print("You've entered a wrong answer to which interest rate. Please try again")
    else:
        print(
            f"For a {interest} Investment of {deposit} at {interest_rate}% for {timeline} years, your total amount "
            f"would be: £{total_investment}"
        )

# Calculations for Bond setting

elif which_calc == "bond":
    value = float(input("Current Value of the property: "))
    interest_rate = float(input("Current APR (interest) rate: "))
    time_taken = float(input("How many months are you taking to repay: "))

    # Calculations for the bonds
    monthly_interest = (interest_rate / 100) / 12
    repayment = round(
        (monthly_interest * value) / (1 - (1 + monthly_interest) ** (-time_taken)), 2
    )

    # Print the final result of the bond
    print(
        f"Your monthly repayments for a property of £{value} at {interest_rate}% APR is £{repayment}/month"
    )

# Catch any issues with the initial choice from user
else:
    print("Please try again and enter either Investment or Bond")
