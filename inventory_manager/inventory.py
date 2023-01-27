# Importing Tabulate for pretty tables
from tabulate import tabulate


class Shoes:
    """
    Defines a Shoe class with attributes country, code, product, cost and quantity
    """

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    # Define the get_cost() method
    def get_cost(self):
        return self.cost

    # Define the get_quantity() method
    def get_quantity(self):
        return self.quantity

    # Define the __str__() method
    def __str__(self):
        # Return the object's attributes as a tuple
        return f"{self.country} {self.code} {self.product} {self.cost} {self.quantity}"


# Create an empty list of shoes
shoes_list = []


def read_shoes_data(file):
    """
    Reads the data from the file and creates a list of Shoe objects
    """
    shoes_list.clear()
    try:
        with open(file, "r", encoding="utf-8") as s_data:
            next(s_data)
            for line in s_data:
                data = line.replace("\n", "").split(",")
                try:
                    shoe_obj = Shoes(data[0], data[1], data[2], data[3], int(data[4]))
                    shoes_list.append(shoe_obj)
                except IndexError:
                    print(
                        "File is incorrectly formatted. Please check the file and try again."
                    )
    except FileNotFoundError:
        print(
            "Sorry, the Inventory file cannot be found.\nPlease ensure it is present before retrying."
        )


def capture_shoes():
    """
    Allows a user to input a new shoe object into the inventory
    """
    # Make code_entry a global to avoid assignment issues later on
    global code_entry
    # Prompt the user to enter the shoe data
    country = input("Enter the country of origin: ").upper()
    # Using a while loop to ensure a code is entered as SKU + 6 digits
    while True:
        try:
            try_code = int(
                input("Enter the product code: SKU").upper().replace(" ", "")
            )
        except ValueError:
            print("Please enter the digits only of the SKU code")
            continue
        else:
            code_entry = "SKU" + str(try_code)
            break
    product = input("Enter the product name: ")
    # Use another while loop to ensure cost is a number
    while True:
        try:
            cost = float(input("Enter the product cost: £").replace(" ", ""))
        except ValueError:
            print("Please enter the cost of the product only.")
        else:
            break
    # Another while loop to ensure quality integer
    while True:
        try:
            quantity = int(input("Enter the quantity: ").replace(" ", ""))
        except ValueError:
            print("Please enter the quantity of the product only.")
        else:
            break
    # Create a Shoe object with the user-entered data
    shoe = Shoes(country, code_entry, product, cost, quantity)

    # Save that to the file
    with open("inventory.txt", "a", encoding="utf-8") as shoe_data:
        shoe_data.writelines(f"\n{country},{code},{product},{cost},{quantity}")
    # Add the Shoe object to the list of shoes
    shoes_list.append(shoe)
    # Return to menu
    print("Shoe successfully saved. Returning to menu.")


def view_all():
    """
    Allow user to view all shoes in a readable table
    """
    read_shoes_data("inventory.txt")
    print("All shoes in inventory:")
    country = []
    code = []
    product = []
    cost = []
    quantity = []
    for idx in range(len(shoes_list)):
        country.append(shoes_list[idx].country)
        code.append(shoes_list[idx].code)
        product.append(shoes_list[idx].product)
        cost.append("£" + str(shoes_list[idx].cost))
        quantity.append(shoes_list[idx].quantity)

    data = {
        "Country": country,
        "Code": code,
        "Product": product,
        "Cost": cost,
        "Quantity": quantity,
    }
    print(
        tabulate(
            data,
            headers=["Country", "Code", "Product", "Cost", "Quantity"],
            tablefmt="fancy_grid",
        )
    )


def re_stock():
    read_shoes_data("inventory.txt")
    # Find the shoe with the lowest quantity
    lowest_quantity = min(shoes_list, key=lambda shoes: shoes.quantity)
    # Output the lowest quantity
    print(
        f"The shoe with the lowest quantity is {lowest_quantity.product} with {lowest_quantity.quantity} in stock."
    )
    # Ask the user if they want to add more of this shoe
    response = input("Do you want to add more of this shoe? (Y/N): ").upper()
    if response == "Y":

        # Ask the user how many shoes they want to add
        quantity = int(input("Enter the quantity to add: "))

        # Add the quantity to the shoe, set the new value to the shoe's quantity
        new_value = int(lowest_quantity.quantity) + quantity
        lowest_quantity.quantity = new_value

        # Save the new quantity to the file
        with open("inventory.txt", "w", encoding="utf-8") as shoe_data:
            shoe_data.write("Country,Code,Product,Cost,Quantity")
            for shoe in shoes_list:
                shoe_data.writelines(
                    f"\n{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}"
                )

        print(f"Successfully added {quantity} to {lowest_quantity.product}.\n")

    # Could use an elif to catch the "N" but catchall is better
    else:
        print("Returning to menu.\n")


def search_shoe():
    """
    Allow user to search for a shoe by name
    """
    # Set global for assignment, set "found" to False
    global search
    found = False

    # Run other function to get the data in a table
    read_shoes_data("inventory.txt")

    # Ask the user to enter the code of the shoe
    while True:
        try:
            search = int(input("Enter the code of the shoe: SKU"))
        except ValueError:
            print("Please enter the digits only of the SKU code")
            continue
        else:
            break

    search_term = "SKU" + str(search)

    # Iterate through the data and get the attributes
    country = []
    code = []
    product = []
    cost = []
    quantity = []
    for idx in range(len(shoes_list)):
        if search_term == shoes_list[idx].code:
            country.append(shoes_list[idx].country)
            code.append(shoes_list[idx].code)
            product.append(shoes_list[idx].product)
            cost.append("£" + str(shoes_list[idx].cost))
            quantity.append(shoes_list[idx].quantity)
            found = True
        else:
            continue

    # Create a dictionary of the data
    data = {
        "Country": country,
        "Code": code,
        "Product": product,
        "Cost": cost,
        "Quantity": quantity,
    }

    # Print the table, using "found" as a condition
    if found:
        print(
            tabulate(
                data,
                headers=["Country", "Code", "Product", "Cost", "Quantity"],
                tablefmt="fancy_grid",
            )
            + "\n"
        )
    else:
        print("No shoes found with that SKU\n")


def value_per_item():
    """
    Returns the value of each item in the inventory
    """

    # Run other function to get the data in a table
    read_shoes_data("inventory.txt")

    # Iterate through the data and get the attributes
    country = []
    code = []
    product = []
    cost = []
    quantity = []
    value = []
    for idx in range(len(shoes_list)):
        country.append(shoes_list[idx].country)
        code.append(shoes_list[idx].code)
        product.append(shoes_list[idx].product)
        cost.append("£" + str(shoes_list[idx].cost))
        quantity.append(shoes_list[idx].quantity)
        new_value = float(shoes_list[idx].cost) * int(shoes_list[idx].quantity)
        value.append("£" + new_value.__format__(".2f"))

    # Create a dictionary of the data
    data = {
        "Country": country,
        "Code": code,
        "Product": product,
        "Cost": cost,
        "Quantity": quantity,
        "Value": value,
    }

    # Print the table
    print("All shoes in inventory:")
    print(
        tabulate(
            data,
            headers=["Country", "Code", "Product", "Cost", "Quantity", "Value"],
            tablefmt="fancy_grid",
        )
    )


def highest_quantity():
    """
    Returns the shoe with the highest quantity
    """

    # Run other function to get the data in a table
    read_shoes_data("inventory.txt")

    # Find the shoe with the highest quantity
    highest_quantity_shoe = max(shoes_list, key=lambda shoes: shoes.quantity)
    # Output the highest quantity
    print("----------------------------------------")
    print(
        f"Quick! {highest_quantity_shoe.product} is selling out!, only {highest_quantity_shoe.quantity} left!"
    )
    print("----------------------------------------\n")


def main_menu():
    menu = """Menu:
    1. Read shoes data
    2. Capture shoes
    3. View all
    4. Re-stock
    5. Search shoe
    6. Value per item
    7. Highest quantity
    8. Exit
    """

    while True:
        print(menu)
        option = input("Enter an option: ")
        if option == "1":
            read_shoes_data("inventory.txt")
        elif option == "2":
            capture_shoes()
        elif option == "3":
            view_all()
        elif option == "4":
            re_stock()
        elif option == "5":
            search_shoe()
        elif option == "6":
            value_per_item()
        elif option == "7":
            highest_quantity()
        elif option == "8":
            break
        else:
            print("Invalid option. Please try again.")


# Run the main menu
if __name__ == "__main__":
    main_menu()
