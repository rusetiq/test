@echo off
setlocal EnableExtensions DisableDelayedExpansion
cd /d "%~dp0"
set "PYTHONHOME="
set "PYTHONPATH="
set "TASK_SETUP_LOG=%CD%\setup-diagnostic.txt"
set "TASK_VENV_PYTHON=%CD%\.venv\Scripts\python.exe"
> "%TASK_SETUP_LOG%" echo Task Management System - Python startup diagnostic

if not exist "task_manager\app.py" goto extract_project
if not exist "requirements.txt" goto extract_project
if not exist "schema.sql" goto extract_project

call :find_python
if defined TASK_PYTHON_EXE goto python_ready
where winget >nul 2>nul
if errorlevel 1 goto python_repair_required
echo Installing the full Python 3.13 distribution...
winget install --id Python.Python.3.13 --exact --source winget --scope user --accept-package-agreements --accept-source-agreements
call :find_python
if not defined TASK_PYTHON_EXE goto python_repair_required

:python_ready
echo Using Python: "%TASK_PYTHON_EXE%"
"%TASK_PYTHON_EXE%" -E -c "import encodings, sys; print(sys.version); print('Python:', sys.executable); print('Standard library:', encodings.__file__)" >> "%TASK_SETUP_LOG%" 2>&1
if not exist "%TASK_VENV_PYTHON%" goto rebuild_environment
"%TASK_VENV_PYTHON%" -E -c "import encodings, pip, sys; from pathlib import Path; assert sys.prefix != sys.base_prefix; assert Path(sys.prefix).resolve() == Path('.venv').resolve()" >> "%TASK_SETUP_LOG%" 2>&1
if not errorlevel 1 goto environment_ready

:rebuild_environment
if not exist ".venv" goto create_environment
set "TASK_BACKUP_NAME=.venv-broken-%RANDOM%-%RANDOM%"
if exist "%TASK_BACKUP_NAME%" goto rebuild_environment
echo Rebuilding the project Python environment. The previous folder will be kept as "%TASK_BACKUP_NAME%".
ren ".venv" "%TASK_BACKUP_NAME%"
if errorlevel 1 goto environment_failed

:create_environment
"%TASK_PYTHON_EXE%" -E -m venv ".venv"
if errorlevel 1 goto environment_failed
"%TASK_VENV_PYTHON%" -E -c "import encodings, pip, sys; from pathlib import Path; assert sys.prefix != sys.base_prefix; assert Path(sys.prefix).resolve() == Path('.venv').resolve()" >> "%TASK_SETUP_LOG%" 2>&1
if errorlevel 1 goto environment_failed

:environment_ready
"%TASK_VENV_PYTHON%" -E -m pip install -r "requirements.txt"
if errorlevel 1 goto dependencies_failed

call :find_mysql
if defined TASK_MYSQL_EXE goto mysql_ready
where winget >nul 2>nul
if errorlevel 1 goto mysql_missing
echo Installing MySQL Server. Follow any installer prompts to configure the server and its password.
winget install --id Oracle.MySQL --exact --accept-package-agreements --accept-source-agreements
call :find_mysql
if not defined TASK_MYSQL_EXE goto mysql_missing

:mysql_ready
set "DB_USER="
set "DB_PASSWORD="
set /p "DB_USER=MySQL username [root]: "
if not defined DB_USER set "DB_USER=root"
set /p "DB_PASSWORD=MySQL password - press Enter if blank: "
set "MYSQL_PWD=%DB_PASSWORD%"
"%TASK_MYSQL_EXE%" -u "%DB_USER%" < "schema.sql"
if errorlevel 1 goto database_failed
set "MYSQL_PWD="
"%TASK_VENV_PYTHON%" -E -c "import json, os; from pathlib import Path; Path('task_manager/mysql_config.json').write_text(json.dumps({'host':'localhost','user':os.environ['DB_USER'],'password':os.environ.get('DB_PASSWORD',''),'database':'task_manager_db'}, indent=2), encoding='utf-8')"
if errorlevel 1 goto settings_failed
set "DB_PASSWORD="
"%TASK_VENV_PYTHON%" -E "task_manager\app.py"
if errorlevel 1 goto application_failed
exit /b 0

:find_python
set "TASK_PYTHON_EXE="
where py >nul 2>nul
if not errorlevel 1 (
    for %%V in (3 3.14 3.13 3.12 3.11 3.10 3.9) do call :probe_launcher %%V
)
for /f "delims=" %%P in ('where python 2^>nul') do call :probe_python "%%P"
for /f "delims=" %%P in ('where python3 2^>nul') do call :probe_python "%%P"
for /d %%D in ("%LocalAppData%\Programs\Python\Python*" "%ProgramFiles%\Python*") do call :probe_python "%%~D\python.exe"
exit /b 0

:probe_launcher
if defined TASK_PYTHON_EXE exit /b 0
for /f "delims=" %%P in ('py -%1 -E -c "import encodings, sys, venv; print(sys.executable)" 2^>nul') do call :probe_python "%%P"
exit /b 0

:probe_python
if defined TASK_PYTHON_EXE exit /b 0
if not exist "%~1" exit /b 0
set "TASK_CANDIDATE=%~1"
if not "%TASK_CANDIDATE:WindowsApps=%"=="%TASK_CANDIDATE%" exit /b 0
>> "%TASK_SETUP_LOG%" echo Checking "%~1"
"%~1" -E -c "import encodings, sys, tkinter, venv; assert sys.version_info >= (3,9); assert sys.prefix == sys.base_prefix" >> "%TASK_SETUP_LOG%" 2>&1
if not errorlevel 1 set "TASK_PYTHON_EXE=%~1"
exit /b 0

:find_mysql
set "TASK_MYSQL_EXE="
for /f "delims=" %%M in ('where mysql 2^>nul') do set "TASK_MYSQL_EXE=%%M"
if defined TASK_MYSQL_EXE exit /b 0
for /d %%D in ("%ProgramFiles%\MySQL\MySQL Server *") do if exist "%%~D\bin\mysql.exe" set "TASK_MYSQL_EXE=%%~D\bin\mysql.exe"
exit /b 0

:extract_project
echo Extract the entire ZIP first, then run windows.bat inside the extracted folder.
goto failed

:python_repair_required
echo Windows could not find a working full Python installation with encodings and Tkinter.
echo Install Python from https://www.python.org/downloads/windows/ with pip and Tcl/Tk enabled.
echo If Python is already installed, open its installer, choose Modify, then Repair.
echo Close this window and run windows.bat again after the repair.
goto failed

:environment_failed
echo The project Python environment could not be created. Repair the full Python installation and try again.
goto failed

:dependencies_failed
echo The Python package installation failed. Check the error above and your internet connection, then try again.
goto failed

:mysql_missing
echo Install and configure MySQL Server from https://dev.mysql.com/downloads/installer/ then run this file again.
goto failed

:database_failed
set "MYSQL_PWD="
set "DB_PASSWORD="
echo MySQL setup failed. Check that MySQL Server is running and your login is correct.
goto failed

:settings_failed
set "DB_PASSWORD="
echo Could not save the local database settings. Check that the project folder is writable.
goto failed

:application_failed
echo The application stopped. Read the error above.

:failed
echo Python startup details are saved in "%TASK_SETUP_LOG%". No MySQL password is included in that log.
pause
exit /b 1
