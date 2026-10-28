# Task Management System

Prepared by **Kasinath Shelly**, with guidance from **Thendral Kala Rajendran**.

A Grade 12 Computer Science practical using Python, Tkinter, and MySQL. It stores tasks with due dates and priorities, and supports search, status filtering, completion, and deletion.

## Quick start

- **Windows:** choose **Extract All** on the ZIP, open the extracted folder, and double-click `windows.bat`. Keep `task_manager`, `schema.sql`, and `requirements.txt` beside the launcher. Do not run the launcher from inside the ZIP.
- **macOS:** run `chmod +x mac.sh && ./mac.sh` in Terminal from the extracted folder.

The launcher creates a Python virtual environment, installs the connector, creates the database from `schema.sql`, saves your MySQL login in `task_manager/mysql_config.json`, and starts the app. On macOS, it can install MySQL with Homebrew when Homebrew is present. On Windows, it looks for a working full Python installation and can install Python 3.13 with winget if needed. It can also install MySQL Server with winget; follow any installer prompts. Enter the MySQL account name and password when requested.

## Windows: encodings not found

`encodings` is part of Python's standard library. Installing an `encodings` package with pip does not repair Python startup.

The updated Windows launcher ignores inherited Python library-path settings and checks that Python can load its standard library and Tkinter before continuing. If the project's `.venv` is broken, it keeps that folder under a `.venv-broken-...` name and creates a fresh environment. It stops when a setup step fails instead of continuing into more errors.

If no working Python is found, the launcher attempts a full Python 3.13 installation through winget. If the installed Python still needs repair, open the Python installer, choose **Modify / Repair**, and include pip and Tcl/Tk. Close the launcher window, then run `windows.bat` again.

If it still fails, open `setup-diagnostic.txt` beside `windows.bat` and share the error lines. That file records Python startup checks and does not contain the MySQL password.

Python reference: [environment variables and the -E option](https://docs.python.org/3/using/cmdline.html#cmdoption-E), [virtual environments](https://docs.python.org/3/library/venv.html).

You can also do the setup manually: install MySQL Server, run `schema.sql`, install `requirements.txt`, set the account in `task_manager/mysql_config.json`, and run `python3 task_manager/app.py`.

## Project files

- [Complete project ZIP](downloads/Kasinath%20Shelly%20-%20Task%20Management%20System.zip)
- [Project report PDF](Task_Management_Project_File.pdf)
- [Illustrative UI preview](Task_Manager_UI_Preview.png)
- [Application](task_manager/app.py), [database functions](task_manager/database.py), and [database configuration](task_manager/db_config.py)

The preview is an illustrative sample screen. The report includes the full source listings, database design, index, and setup instructions.
