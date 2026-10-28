#!/bin/bash
set -e
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is required. Install it from https://www.python.org/downloads/macos/ and run this script again."
    exit 1
fi

if ! command -v mysql >/dev/null 2>&1; then
    if command -v brew >/dev/null 2>&1; then
        brew install mysql
    else
        echo "MySQL is required. Install Homebrew from https://brew.sh, then run this script again."
        exit 1
    fi
fi

if command -v brew >/dev/null 2>&1; then
    brew services start mysql >/dev/null
fi

if [ ! -d .venv ]; then
    python3 -m venv .venv
fi
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt

printf "MySQL username [root]: "
read -r DB_USER
DB_USER=${DB_USER:-root}
printf "MySQL password (leave blank if none): "
read -r -s DB_PASSWORD
printf "\n"

MYSQL_PWD="$DB_PASSWORD" mysql -u "$DB_USER" < schema.sql
DB_USER="$DB_USER" DB_PASSWORD="$DB_PASSWORD" DB_NAME="task_manager_db" python3 - <<'PYCONFIG'
import json
import os
from pathlib import Path

config = {"host": "localhost", "user": os.environ["DB_USER"], "password": os.environ["DB_PASSWORD"], "database": os.environ["DB_NAME"]}
Path("task_manager/mysql_config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
PYCONFIG

.venv/bin/python "task_manager/app.py"
