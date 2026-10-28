CREATE DATABASE IF NOT EXISTS task_manager_db;
USE task_manager_db;

CREATE TABLE IF NOT EXISTS tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description VARCHAR(255),
    due_date DATE,
    priority VARCHAR(10) NOT NULL DEFAULT 'Normal',
    status VARCHAR(15) NOT NULL DEFAULT 'Pending'
);
