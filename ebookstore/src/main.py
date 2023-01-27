# Capstone V: Bookstore
# Author: Matthew Butcher (mbutcher.dev)
# GitHub: mbutcherdev
# Date: 01-2023

# Import modules
import sqlite3
import datetime
import os
from menu import *
from tabulate import tabulate

# Pre-populated list for the database. Add here before running the program if they're consistent across runs
book_list = [
    (3001, "A Tale of Two Cities", "Charles Dickens", 30),
    (3002, "Harry Potter and the Philosopher's Stone", "J.K. Rowling", 40),
    (3003, "The Lion, the Witch and the Wardrobe", "C.S. Lewis", 25),
    (3004, "The Lord of the Rings", "J.R.R Tolkien", 37),
    (3005, "Alice in Wonderland", "Lewis Carroll", 12),
    (3006, "The Hobbit", "J.R.R Tolkien", 22)
]


class BookDatabase(object):
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()

    # Create the table
    def create(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, title TEXT, author TEXT, quantity INTEGER)")
        self.commit()

    # All queries will be executed from here
    def query(self, arg):
        self.cur.execute(arg)
        return self.cur

    def insert(self, *args):
        self.cur.execute('INSERT INTO books VALUES (?, ?, ?, ?)', args)
        self.commit()

    def delete(self, *args):
        self.cur.execute("DELETE FROM books WHERE id=?", args)
        self.commit()

    # Using exists to check a record is within the database, returning t/f.
    # This prevents trying to display something that doesn't exist and hitting errors
    def exists(self, arg):
        self.cur.execute(arg)
        if self.cur.fetchone() is None:
            return False
        else:
            return True

    # Tabulate is used to display the query results in a table, headers are static.
    # Change the headers if you change the database keys
    def pretty_query(self, arg):
        headers = ["ID", "Title", "Author", "Quantity"]
        data = self.cur.execute(arg)
        return tabulate(data, headers=headers, tablefmt="rounded_grid")

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


# I wanted a way to log when the program was started/exited.
# This is a simple iteration of that. I could also open a logfile but unnecessary at this point
def get_date_time():
    now = datetime.datetime.now()
    return now.strftime("%m-%d-%Y %H:%M:%S")


# We initially check if the /data path exists, followed by checking if the ebookstore.db exists
# We make the directory if it doesn't exist, and create the database if it doesn't exist
# Set "dbms" - Database Management System as a new instance of the BookDatabase class
try:
    if not os.path.exists("./data"):
        os.makedirs("./data")
    dbms = BookDatabase("data/ebookstore.db")
    print(f"Connection to database successful: {get_date_time()}")
except sqlite3.OperationalError:
    print(f"Error: Could not connect to database: {get_date_time()}")


# We check if the database exists within sqlite_master, if it doesn't we call create
def create_table():
    try:
        check = dbms.exists("SELECT name FROM sqlite_master WHERE type='table' AND name='books';")
        if not check:
            print("Table does not exist. Creating table...")
            dbms.create()
        else:
            print("Table exists. Moving on...")
    except sqlite3.OperationalError:
        print("Error: Could not create table.")


# Using the pre-existing list to populate the database. This is only run once.
# To run again the database has to be deleted entirely.
# This is to prevent duplicate entries.
def insert_data():
    try:
        for book in book_list:
            dbms.insert(book[0], book[1], book[2], book[3])
        print("Data doesn't exist. Writing...")
        dbms.commit()
    except sqlite3.OperationalError:
        print("Error: Could not insert data.")
    except sqlite3.IntegrityError:
        print("Book list exists. Moving on...")


# Performs a simple grab all from database, using Tabulate to display the results
def current_stock():
    try:
        check = dbms.exists("SELECT * FROM books")
        if check:
            print("-------------------")
            print(dbms.pretty_query("SELECT * FROM books"))
            print("-------------------")
        else:
            print("No books in stock.")
    except sqlite3.OperationalError:
        print("Error: Could not show current stock.")


# Grab all details for new book from user, insert into database and confirm
def add_book():
    book_id = dbms.query("SELECT MAX(id) FROM books").fetchone()[0] + 1
    title = input("Enter the book title: ")
    author = input("Enter the book author: ")
    quantity = input("Enter the book quantity: ")
    try:
        dbms.insert(book_id, title, author, quantity)
        print("Book added successfully.")
        dbms.commit()
    except sqlite3.OperationalError:
        print("Error: Could not add book.")
    except sqlite3.IntegrityError:
        print("Book already exists.")


# Print the current stock, grab ID to delete from user, confirmation and then removal
def delete_book():
    current_stock()
    book_id = input("Enter the book ID to delete: ")
    try:
        check = dbms.exists(f"SELECT * FROM books WHERE id={book_id}")
        if check:
            print("Book exists. Deleting...")
            dbms.query(f"DELETE FROM books WHERE id={book_id}")
            print("Book deleted successfully.")
            dbms.commit()
        else:
            print("Book does not exist.")
    except Exception as e:
        print("Error: Could not delete book.")
        print(e)


# Search function allowing by multiple methods. We use %wildcards% to grab any matching results
# This acts like a real bookstore system when you may only know a word of the title
def search_book():
    print("Search the e-shelves:")
    print("1. Search by title")
    print("2. Search by author")
    print("3. Search by ID")
    print("0. Return to main menu")
    choice = input("Enter your choice: ")
    if choice == "1":
        title = input("Enter the book title: ")
        title = str("%" + title + "%")  # Allow wildcard searches
        try:
            check = dbms.exists(f"SELECT * FROM books WHERE title LIKE '{title}'")
            if check:
                print(dbms.pretty_query(f"SELECT * FROM books WHERE title LIKE '{title}'"))
            else:
                print("No books found.")

        except sqlite3.OperationalError:
            print("Error: Could not search for book.")
    elif choice == "2":
        author = input("Enter the book author: ")
        author = str("%" + author + "%")  # Allow wildcard searches
        try:
            check = dbms.exists(f"SELECT * FROM books WHERE author LIKE '{author}'")
            if check:
                print(dbms.pretty_query(f"SELECT * FROM books WHERE author LIKE '{author}'"))
            else:
                print("No books found.")
        except sqlite3.OperationalError:
            print("Error: Could not search for book.")
    elif choice == "3":
        book_id = input("Enter the book ID: ")
        book_id = str("%" + book_id + "%")  # Allow wildcard searches
        try:
            check = dbms.exists(f"SELECT * FROM books WHERE id LIKE '{book_id}'")
            if check:
                print(dbms.pretty_query(f"SELECT * FROM books WHERE id LIKE '{book_id}'"))
            else:
                print("No books found.")
        except sqlite3.OperationalError:
            print("Error: Could not search for book.")
    elif choice == "0":
        return


# Fetch the ID of the book, if it exists we can update the quantity field
def change_stock():
    current_stock()
    choice = input("Please enter ID of the book you'd like to update: ")
    try:
        check = dbms.exists(f"SELECT * FROM books WHERE id = {choice}")
        if check:
            dbms.pretty_query(f"SELECT * FROM books WHERE id = {choice}")
            quantity = input("Please enter the new quantity: ")
            dbms.query(f"UPDATE books SET quantity = {quantity} WHERE id = {choice}")
            print("Stock updated successfully.")
            dbms.commit()
    except sqlite3.OperationalError:
        print("Error: Could not update stock.")


# Closing down the program. Commit any changes, kill the connection and then exit with timestamp
def stop():
    dbms.commit()
    dbms.close()
    print(f"Database connection closed")
    print("Thank you for using the E-Bookstore management system.")
    print(f"System exit at: {get_date_time()}")
    quit()


# When the program starts, it will check if the table exists. If not, it will create it.
# If the table exists, it will check if the data exists. If not, it will insert the data.
# After that we display the menu from the other module
def set_up():
    try:
        create_table()
        insert_data()
        print("Initial set-up complete. Loading Menu...\n")
        print("-------------------")
        menu = Menu()
        menu.make_choice()
    except sqlite3.OperationalError:
        print("Error: Could not set up database.")
        print("Exiting program...")
        quit()


if __name__ == "__main__":
    set_up()
