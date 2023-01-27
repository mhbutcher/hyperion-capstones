from main import current_stock, add_book, delete_book, search_book, change_stock, stop


# Menu options
class Menu:
    def __init__(self):
        self.choices = {
            "1": current_stock,
            "2": add_book,
            "3": delete_book,
            "4": search_book,
            "5": change_stock,
            "0": stop,
        }

    @staticmethod
    def make_choice():
        choice = ""
        while choice != "0":
            print(
                """
E-Bookstore Management System
1. View current stock
2. Add a book
3. Delete a book
4. Search for a book
5. Change stock
0. Quit
            """
            )
            choice = input("Enter your choice: ")
            # Check if choice is within the dictionary and run the associated function
            if choice in Menu().choices:
                Menu().choices[choice]()
            else:
                print("Invalid choice.")
