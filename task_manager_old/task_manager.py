# =====importing libraries===========
from datetime import date

# ====Login Section====
# Access the user.txt file and store values in a list.
user_login = []
user_password = []

with open("user.txt", "r") as file:
    for line in file:
        username = line.split(", ")
        username = [nline.replace("\n", "") for nline in username]
        user_login.append(username[0])
        user_password.append(username[1])

# Check for username in the correct list, if found we'll grab the matching password location
# Check the password attempt for the matching index in the second list
while True:
    username_attempt = input("Please enter username: ")
    if username_attempt in user_login:
        password_location = user_login.index(username_attempt)
        password_attempt = input("Please enter password: ")
        if password_attempt == user_password[password_location]:
            print("You have successfully logged in.")
            # Set the username, for personalization in menu and admin check
            user = username_attempt
            break
        else:
            print("Incorrect Password.")
    else:
        print("Incorrect Username. Please try again.")

# Storing a list here to get total task count outside the while loop
task_list = []

# Decide which menu to show to the user
while True:
    if user != "admin":
        menu = input(
            f"""Please select one of the following options:
    r - Register a new user
    a - Add a new task
    va - View all tasks
    vm - View tasks currents assigned to {user}
    e - Exit
    Selection: """
        ).lower()
    if user == "admin":
        menu = input(
            f"""Please select one of the following options:
    r - Register a new user
    a - Add a new task
    va - View all tasks
    vm - View tasks currents assigned to {user}
    s - {user} only option. View Statistics on Users and Tasks
    e - Exit
    Selection: """
        ).lower()

    # If admin selects Register new user, otherwise exit
    # First get username, password. Check password is correct against supplied password
    # If correct append to the user file, else send back to menu
    if menu == "r":
        if user == "admin":
            with open("user.txt", "a") as newuser:
                while True:
                    new_username = input("Enter a new username: ")
                    new_password = input(f"Enter a new password for {new_username}: ")
                    new_password_check = input(
                        f"Confirm new password for {new_username}: "
                    )
                    if new_password == new_password_check:
                        newuser.write(
                            "\n" + str(new_username) + ", " + str(new_password)
                        )
                        print(f"User {new_username} created by {user} successfully.\n")
                        break
                    else:
                        print("Passwords did not match.\n")
                        break
        else:
            print(f"Sorry {user}, only admin can register new users.\n")

    # This will allow users to add new tasks to the task file
    elif menu == "a":
        print("Adding new task: ")
        with open("tasks.txt", "a") as task_file:
            assigned = input("Assign task to: ")
            task_title = input("Task Title: ")
            task_description = input("Task Description: ")
            task_due_date = input("Task Due Date: ")
            # Use datetime to import today's date into the task creation
            task_set_date = str(date.today().strftime("%d %B %Y"))
            task_complete = "No"
            task_file.write(
                "\n"
                + assigned
                + ", "
                + task_title
                + ", "
                + task_description
                + ", "
                + task_due_date
                + ", "
                + task_set_date
                + ", "
                + task_complete
            )
            print("Task added successfully\n")

    # Enables user to see all tasks assigned
    elif menu == "va":
        print("All current tasks: ")
        with open("tasks.txt", "r") as all_tasks:
            for tasks in all_tasks:
                task_file = tasks.split(", ")
                # Tasks are assign 0, title 1, desc 2, due 3, set 4, complete 5
                print("-------------------------------")
                print(
                    f"""    Task:           {task_file[1]}
    Assigned to:    {task_file[0]} 
    Date Assigned:  {task_file[4]}
    Date Due:       {task_file[3]} 
    Task Complete?: {task_file[5]}
    Task Description:
        {task_file[2]}
                """
                )
        print("-------------------------------")

    # User views their own tasks.
    # Using same format as view all to output, check if index [0] matches user
    elif menu == "vm":
        print("Your current tasks: ")
        with open("tasks.txt", "r") as my_tasks:
            for tasks in my_tasks:
                m_tasks = tasks.split(", ")
                if m_tasks[0] == user:
                    print("-------------------------------")
                    print(
                        f"""    Task:           {m_tasks[1]}
    Assigned to:    {m_tasks[0]} 
    Date Assigned:  {m_tasks[4]}
    Date Due:       {m_tasks[3]} 
    Task Complete?: {m_tasks[5]}
    Task Description:
        {m_tasks[2]}
                """
                    )
        print("-------------------------------")

    # Menu option to exit the project
    elif menu == "e":
        print("Thanks for using Task Manager\nGoodbye!")
        exit()

    # Admin menu to see stats about total users from user_name list and task_list
    elif menu == "s":
        if user == "admin":
            print("Total Users: " + str(len(user_login)))
            with open("tasks.txt", "r") as task_file:
                for tasks in task_file:
                    total = tasks.split(", ")
                    task_list.append(total)
            print("Total Tasks: " + str(len(task_list)))
    # Incorrect choice error handling
    else:
        print("Incorrect choice made, please retry.")
