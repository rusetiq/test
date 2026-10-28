import mysql.connector

from db_config import DB_CONFIG


def connect():
    return mysql.connector.connect(**DB_CONFIG)


def create_table():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tasks (
            task_id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(100) NOT NULL,
            description VARCHAR(255),
            due_date DATE,
            priority VARCHAR(10) NOT NULL DEFAULT 'Normal',
            status VARCHAR(15) NOT NULL DEFAULT 'Pending'
        )"""
    )
    cursor.execute("SHOW COLUMNS FROM tasks LIKE 'priority'")
    if not cursor.fetchone():
        cursor.execute("ALTER TABLE tasks ADD priority VARCHAR(10) NOT NULL DEFAULT 'Normal'")
    connection.commit()
    cursor.close()
    connection.close()


def get_tasks(search_text="", status="All"):
    connection = connect()
    cursor = connection.cursor()
    query = "SELECT task_id, title, description, due_date, priority, status FROM tasks WHERE (title LIKE %s OR description LIKE %s)"
    values = [f"%{search_text}%", f"%{search_text}%"]
    if status != "All":
        query += " AND status = %s"
        values.append(status)
    query += " ORDER BY CASE priority WHEN 'High' THEN 1 WHEN 'Normal' THEN 2 ELSE 3 END, due_date, task_id"
    cursor.execute(query, tuple(values))
    tasks = cursor.fetchall()
    cursor.close()
    connection.close()
    return tasks


def add_task(title, description, due_date, priority):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, description, due_date, priority) VALUES (%s, %s, %s, %s)",
        (title, description, due_date, priority),
    )
    connection.commit()
    cursor.close()
    connection.close()


def complete_task(task_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("UPDATE tasks SET status = 'Completed' WHERE task_id = %s", (task_id,))
    connection.commit()
    changed = cursor.rowcount
    cursor.close()
    connection.close()
    return changed > 0


def delete_task(task_id):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
    connection.commit()
    changed = cursor.rowcount
    cursor.close()
    connection.close()
    return changed > 0
