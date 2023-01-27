# =====importing libraries===========
from datetime import date

# ========= Functions ===========

# ===== User Check =====
# Call to update internal list on current users


def users_check():
    # Clear existing entries from the list
    user_login.clear()
    user_password.clear()
    with open("user.txt", "r") as file:

        # Grab the user file, split the data and add to a login and password list
        for line in file:
            username = line.split(", ")
            username = [nline.replace("\n", "") for nline in username]
            user_login.append(username[0])
            user_password.append(username[1])


# ===== Add User =====
# Call to add new users to the user file, if admin


def add_user():
    # Grab updated version of user list, useful if adding multiple in a row
    users_check()
    if user == "admin":
        with open("user.txt", "a") as newuser:
            while True:
                new_username = input("Enter a new username: ")

                # Check if the username already exists in the list
                if new_username in user_login:
                    print(
                        f'Username: "{new_username}" already exists in system. Please try again.'
                    )
                else:
                    new_password = input(
                        f"Enter a new password for {new_username}: "
                    )
                    new_password_check = input(
                        f"Confirm new password for {new_username}: "
                    )

                    # Ensure passwords match before moving on
                    if new_password == new_password_check:
                        # Write the new username and password combo to the open file, confirm to user
                        newuser.write(
                            "\n" + str(new_username) + ", " + str(new_password)
                        )
                        print(
                            f"User {new_username} created by {user} successfully.\n"
                        )
                        break
                    else:
                        print("Passwords did not match.\n")
                        break

    # If not logged in as admin, do not allow new members to be created
    else:
        print(f"Sorry {user}, only admin can register new users.\n")


# ===== Add New Task =====
# Call to add new tasks to the tasks.txt file


def add_task():
    print("Adding new task: ")

    # Refresh the tasks list
    update_tasks()
    users_check()
    curr_task_number = int(len(task_list) + 1)
    with open("tasks.txt", "a+") as task_file:

        # Set variables from the user
        assigned_to = input("Assign task to: ")
        if assigned_to in user_login:
            task_title = input("Task Title: ")
            task_description = input("Task Description: ")
            task_due_date = input("Task Due Date: ")

            # Use datetime to import today's date into the task creation
            task_set_date = str(date.today().strftime("%d/%m/%Y"))
            task_complete = "No"

            # Write the new details to the file
            task_file.write(
                str(curr_task_number)
                + "; "
                + assigned_to
                + "; "
                + task_title
                + "; "
                + task_description
                + "; "
                + task_due_date
                + "; "
                + task_set_date
                + "; "
                + task_complete
                + "\n"
            )

            # Confirm to the user the tasks has been added
            print("Task added successfully\n")
        else:
            print("User not in system.\n")


# ===== View All Tasks =====
# Call to view all tasks currently in the tasks file


def view_all():
    # Refresh the tasks list
    update_tasks()
    print("\nAll current tasks: \n")
    for idx in task_list:

        # Iterate through the task list and print out results in a readable format
        print(
            f"Task Number:\t{idx[0]}\nTask Name:\t{idx[2]}\nAssigned to:\t{idx[1]}\nAssigned date:\t{idx[5]}\nDue Date:\t{idx[4]}\nComplete:\t{idx[6]}\nDescription:\t{idx[3]}\n"
        )


# ===== View My Tasks =====
# Call to view current users tasks. Allows for editing of tasks


def view_mine():
    # Refresh the tasks list
    update_tasks()

    # Set user for use later in the loop
    username = user
    print(f"\nTasks for:\t {username} \n")
    for idx in task_list:

        # Check if the current 'Assigned to' value is equal to username
        if idx[1] == username:

            # For entries where username matches, print out to user in readable format
            print(
                f"Task Number:\t{idx[0]}\nTask Name:\t{idx[2]}\nAssigned to:\t{idx[1]}\nAssigned date:\t{idx[5]}\nDue Date:\t{idx[4]}\nComplete:\t{idx[6]}\nDescription:\t{idx[3]}\n"
            )
    try:

        # Use a Try/Except method here to catch any entires that aren't an int
        edit = int(input("Enter Task number or exit (-1): "))

        # Options for editing the task if entry was not -1
        if edit != "-1":

            # Change the task number to a string
            task_number = str(edit)
            for idxs in task_list:

                # Check if the task number and username match the current user
                if idxs[0] == task_number and idxs[1] == username:

                    # idxs[6] is the completed value
                    if idxs[6] == "No":
                        is_complete = input(
                            "Mark as complete (y/n) or edit task? (e): "
                        ).lower()

                        # Check if task is being completed or requires editing
                        # Update the required field and pass to the save_tasks() function
                        if is_complete == "y":
                            idxs[6] = "Yes"
                            save_tasks()
                            break
                        elif is_complete == "n":
                            print("No changes made.")
                            break
                        elif is_complete == "e":

                            # If edit is selected, choose reassign or due date
                            # Check both on the if statements and pass to save_tasks
                            choice = str(
                                input(
                                    "Would you like to Reassign (r) or Change Due date (d): "
                                )
                            )
                            if choice == "r":

                                # Refresh the user list and check username entered exists
                                users_check()
                                new_username = str(
                                    input("Enter new username: ")
                                )

                                # Change the list entry and call save_tasks() or break out if it doesn't exist
                                if new_username in user_login:
                                    idxs[1] = new_username
                                    save_tasks()
                                    print("Task Reassigned")
                                    break
                                else:
                                    print("User does not exist")
                                    break

                            # Change entry in list and call save_tasks() on date
                            elif choice == "d":
                                new_date = input(
                                    "Please enter the new due date (DD/MM/YYYY format): "
                                )
                                idxs[4] = new_date
                                save_tasks()
                                break

                    # If the tasks is completed, tell user and break loop
                    else:
                        print("Cannot edit completed task")
                        break

    # Catch ValueError for non-int inputs of task number
    except ValueError:
        print("Please enter a number.")


# ===== Statistics =====
# Call to view statistics if logged in as Admin


def stats():
    # Refresh the users list and tasks list
    # Print total users and then total tasks
    users_check()
    user_total = len(user_login)
    print("\n-------------------------")
    print(f"Total Users: {user_total}")
    update_tasks()
    print("Total Tasks: " + str(len(task_list)))
    # Run the reports function to ensure the overview files are created
    # Loop through the lines and print to console
    generate_reports()
    with open("task_overview.txt", "r") as t_file:
        for line in t_file:
            print(line)
    with open("user_overview.txt", "r") as u_file:
        for line in u_file:
            print(line)


# ===== Update Tasks =====
# Function to update the task list with data from the file


def update_tasks():
    # Clear the current list
    task_list.clear()
    with open("tasks.txt", "r") as task_file:
        data = [line.strip() for line in task_file]
    # Split the file and add to the list
    for line in data:
        task_list.append(line.split("; "))


# ===== Save Tasks =====
# Function to save the current task list to the file


def save_tasks():
    # Open the tasks file, 'w' mode to wipe current data
    # Iterate through the tasks_list and use ; as the split value
    # Write the new data to the file
    with open("tasks.txt", "w") as file_handle:
        for item in task_list:
            new_file = "; ".join(map(str, item))
            file_handle.write(f"{new_file}\n")


# ===== Generate Reports =====
# Allows Admin users to generate readable files of important information


def generate_reports():
    # Refresh the tasks list, set initial variables
    update_tasks()
    task_number = len(task_list)
    complete = 0
    incomplete = 0
    overdue = 0
    todays_date = date.today().strftime("%d/%m/%Y")
    incomp_percent = round(((incomplete / task_number) * 100), 2)
    overdue_percent = round(((overdue / task_number) * 100), 2)

    # Iterate through the tasks list, match complete/incomplete/overdue and add to variable
    for idx in task_list:
        due_date = idx[4]
        if idx[6] == "Yes":
            complete += 1
        elif idx[6] == "No":
            incomplete += 1
            if due_date.strip() < todays_date.strip():
                overdue += 1

    incomp_percent = round(((incomplete / task_number) * 100), 2)

    # Using a try/except loop here for cases where task - complete = 0
    try:
        overdue_percent = round(
            ((overdue / (task_number - complete)) * 100), 2
        )
    except ZeroDivisionError:
        overdue_percent = 0

    # Write the data to the task_overview in a readable format
    with open("task_overview.txt", "w") as t_overview:
        t_overview.write(
            "----------------------------------------------------------------\n"
        )

        t_overview.write(
            f"Report for:                             {todays_date}\n"
        )
        t_overview.write(
            f"Number of total tasks:                  {task_number}\n"
        )
        t_overview.write(
            f"Number of completed tasks:              {complete}\n"
        )
        t_overview.write(
            f"Number of incomplete tasks:             {incomplete}\n"
        )
        t_overview.write(
            f"Number of tasks incomplete and overdue: {overdue}\n"
        )
        t_overview.write(
            f"Percentage of tasks incomplete:         {incomp_percent}%\n"
        )
        t_overview.write(
            f"Percentage of tasks now overdue:        {overdue_percent}%\n"
        )

        t_overview.write(
            "----------------------------------------------------------------"
        )

    # User_overview
    # Refresh the users list
    users_check()
    user_total = len(user_login)

    # Open the file and start writing in a readable format
    with open("user_overview.txt", "w") as u_overview:
        u_overview.write(f"Total users: {user_total}\n")
        u_overview.write(f"Total Tasks: {task_number}\n")

        # Iterate through user_login list and check tasks
        for idx in user_login:
            task_count_each = 0
            completed_each = 0
            incomplete_each = 0
            overdue_each = 0
            for tasks in task_list:
                if idx == tasks[1]:
                    task_count_each += 1
                    if tasks[6] == "Yes":
                        completed_each += 1
                    elif tasks[6] == "No":
                        incomplete_each += 1
                        if due_date.strip() < todays_date.strip():
                            overdue_each += 1

            # Try statements for the rest, always catching ZeroDivision
            # If a user has no tasks/none incomplete/overdue it'll return 0
            try:
                percent_of_tasks = round(
                    ((task_count_each / task_number) * 100), 2
                )
            except ZeroDivisionError:
                percent_of_tasks = 0
            try:
                percent_complete = round(
                    ((completed_each / task_count_each) * 100), 2
                )
            except ZeroDivisionError:
                percent_complete = 0
            try:
                percent_incomplete = round(
                    ((incomplete_each / task_count_each) * 100), 2
                )
            except ZeroDivisionError:
                percent_incomplete = 0
            try:
                percent_overdue = round(
                    (
                        (overdue_each / (task_count_each - completed_each))
                        * 100
                    ),
                    2,
                )
            except ZeroDivisionError:
                percent_overdue = 0

            # Continue writing to the file in a readable format
            u_overview.write(f"------------------------------------------\n")
            u_overview.write(f"Report for user:                 {idx}\n")
            u_overview.write(
                f"Total tasks assigned:            {task_count_each}\n"
            )
            u_overview.write(
                f"Percentage of tasks assigned:    {percent_of_tasks}%\n"
            )
            u_overview.write(
                f"Percent of tasks completed:      {percent_complete}%\n"
            )
            u_overview.write(
                f"Percentage of tasks incomplete:  {percent_incomplete}%\n"
            )
            u_overview.write(
                f"Percentage of tasks now overdue: {percent_overdue}%\n"
            )
            u_overview.write(f"------------------------------------------\n")


# ===== Login =====
# Function to check login details are valid, assign user for TaskManager use


def login():
    while True:
        # Refresh the current user list
        users_check()
        username_attempt = input("Please enter username: ")

        # Check the entered username exists in the list
        if username_attempt in user_login:

            # If username exists, grab the index and use that for the password list
            password_location = user_login.index(username_attempt)
            password_attempt = input("Please enter password: ")

            # If the password matches the index in list, accept user
            if password_attempt == user_password[password_location]:
                print("You have successfully logged in.")

                # Set the username, for personalization in menu and admin check
                return username_attempt
            else:
                print("Incorrect Password.")
        else:
            print("Incorrect Username. Please try again.")


# ===== Menu =====
# Display a user and admin menu, each option calls a function


def menu():
    while True:

        # Menu if user is not set to admin
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

        # Admin only menu
        if user == "admin":
            menu = input(
                f"""Please select one of the following options:
        r - Register a new user
        a - Add a new task
        va - View all tasks
        vm - View tasks currents assigned to {user}
        ds - {user} only option. View Statistics on Users and Tasks
        gr - {user} only option. Generate Task and User Reports
        e - Exit
        Selection: """
            ).lower()

        # Add new users to the program
        if menu == "r":
            add_user()

        # This will allow users to add new tasks to the task file
        elif menu == "a":
            add_task()

        # Enables user to see all tasks assigned
        elif menu == "va":
            view_all()

        # User views their own tasks.
        elif menu == "vm":
            view_mine()

        # Menu option to exit the project
        elif menu == "e":
            print("Thanks for using Task Manager\nGoodbye!")
            exit()

        # Option to display statistics about the program
        elif menu == "ds":
            if user == "admin":
                stats()
            else:
                print("Admin only command.\n")

        # Option to create reports(files) about the statistics
        elif menu == "gr":
            if user == "admin":
                generate_reports()
            else:
                print("Admin only command.\n")

        # Incorrect choice error handling
        else:
            print("Incorrect choice made, please retry.")
        pass


# Set initial lists to be used throughout the program
user_login = []
user_password = []
task_list = []

# Start the application by setting user to the login function
# Once user is logged in, call the Menu loop
user = login()
menu()
