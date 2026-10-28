import json
from pathlib import Path

CONFIG_FILE = Path(__file__).with_name("mysql_config.json")
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "your_mysql_password",
    "database": "task_manager_db",
}
if CONFIG_FILE.exists():
    DB_CONFIG.update(json.loads(CONFIG_FILE.read_text(encoding="utf-8-sig")))
