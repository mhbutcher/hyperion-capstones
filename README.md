
# HyperionDev - Capstone Projects

A collection of first-iteration projects completed for the HyperionDev Software Engineering bootcamp.

| Capstone    | Project Title | Description|
| -- | -- | --|
| Capstone I| Finance Calculator| CLI application for investment/bond calculations |
| Capstone II   | Task Manager (old)| CLI application for managing tasks for users|
| Capstone III| Task Manager| CLI application with OOP for managing tasks for users|
| Capstone IV| Inventory Manager| CLI application to replicate interaction with a file-based stock system for a shoe brand/store|
|Capstone V| E-bookstore| CLI application build to replicate a library or bookstore management system. Uses a SQLite3 database system to store entries into the database.|




## Tech Stack

Python3, SQLite3, Tabulate



## Run Locally

Clone the project

```bash
  git clone https://github.com/mbutcherdev/hyperion-capstones
```

Go to the project directory which you'd like to run

```bash
  cd finance_calculator
  cd task_manager_old
  cd task_manager
  cd inventory_manager
  cd ebookstore
```

Install dependencies

```bash
  pip -r requirements.txt 
```

Run the project (use the appropriate filename, ending in .py)

```bash
  python project_filename.py
```


## Lessons Learned

- Python3 is an incredible language  
These capstones allowed me to see how the Python programming language could be used to display cli applications to a user. I'd already known some of the language so it was a good chance to renew that knowlege and put it towards projects that resemble some real-world examples.

- SQL  
I've previously had experience with MySQL so the transition into SQLite was quite painless. After building the project and including f-string searches, I realised that if this was a real-world application, the risk of SQL Injection is built into my code.
This is currently being corrected and will be fixed either in the ebookstore directory or as a standalone GUI application.

- Tabulate  
Tabulate (https://pypi.org/project/tabulate/) is an amazing module, allowing the display of results from lists or database queries. This makes for a much better experience rather than the standard output.


## Authors

- [@mbutcherdev](https://www.github.com/mbutcherdev)

