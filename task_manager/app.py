import tkinter as tk
from tkinter import messagebox, ttk

import database


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Management System")
        self.root.geometry("930x590")
        self.root.minsize(720, 460)
        self.selected_task_id = None
        self.setup_style()
        self.build_screen()
        self.refresh_tasks()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f4f6fb")
        style.configure("TLabel", background="#f4f6fb", foreground="#26324a")
        style.configure("Title.TLabel", font=("Arial", 22, "bold"), foreground="#172554")
        style.configure("Hint.TLabel", font=("Arial", 10), foreground="#64748b")
        style.configure("TButton", font=("Arial", 10), padding=(12, 8))
        style.configure("Accent.TButton", background="#315efb", foreground="white")
        style.map("Accent.TButton", background=[("active", "#2448c9")])
        style.configure("Treeview", rowheight=32, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    def build_screen(self):
        page = ttk.Frame(self.root, padding=24)
        page.pack(fill="both", expand=True)

        ttk.Label(page, text="My Tasks", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            page,
            text="Add tasks, track due dates, and mark finished work.",
            style="Hint.TLabel",
        ).pack(anchor="w", pady=(4, 18))

        form = ttk.Frame(page)
        form.pack(fill="x", pady=(0, 16))
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Task title").grid(row=0, column=0, sticky="w", padx=(0, 10), pady=5)
        self.title_entry = ttk.Entry(form)
        self.title_entry.grid(row=0, column=1, sticky="ew", pady=5)

        ttk.Label(form, text="Description").grid(row=1, column=0, sticky="w", padx=(0, 10), pady=5)
        self.description_entry = ttk.Entry(form)
        self.description_entry.grid(row=1, column=1, sticky="ew", pady=5)

        ttk.Label(form, text="Due date").grid(row=2, column=0, sticky="w", padx=(0, 10), pady=5)
        self.date_entry = ttk.Entry(form)
        self.date_entry.grid(row=2, column=1, sticky="ew", pady=5)
        self.date_entry.insert(0, "YYYY-MM-DD")

        ttk.Label(form, text="Priority").grid(row=3, column=0, sticky="w", padx=(0, 10), pady=5)
        self.priority_choice = ttk.Combobox(form, values=("Low", "Normal", "High"), state="readonly")
        self.priority_choice.grid(row=3, column=1, sticky="w", pady=5)
        self.priority_choice.set("Normal")

        self.add_button = ttk.Button(
            form, text="Add task", style="Accent.TButton", command=self.add_task
        )
        self.add_button.grid(row=0, column=2, rowspan=4, padx=(14, 0), sticky="ns")

        filters = ttk.Frame(page)
        filters.pack(fill="x", pady=(0, 8))
        ttk.Label(filters, text="Search").pack(side="left")
        self.search_entry = ttk.Entry(filters, width=28)
        self.search_entry.pack(side="left", padx=8)
        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh_tasks())
        ttk.Label(filters, text="Status").pack(side="left", padx=(12, 4))
        self.status_choice = ttk.Combobox(filters, values=("All", "Pending", "Completed"), state="readonly", width=12)
        self.status_choice.set("All")
        self.status_choice.pack(side="left")
        self.status_choice.bind("<<ComboboxSelected>>", lambda event: self.refresh_tasks())

        table_frame = ttk.Frame(page)
        table_frame.pack(fill="both", expand=True)

        columns = ("id", "title", "description", "due_date", "priority", "status")
        self.task_table = ttk.Treeview(
            table_frame, columns=columns, show="headings", selectmode="browse"
        )
        self.task_table.heading("id", text="ID")
        self.task_table.heading("title", text="TASK")
        self.task_table.heading("description", text="DESCRIPTION")
        self.task_table.heading("due_date", text="DUE DATE")
        self.task_table.heading("priority", text="PRIORITY")
        self.task_table.heading("status", text="STATUS")
        self.task_table.column("id", width=50, anchor="center", stretch=False)
        self.task_table.column("title", width=180)
        self.task_table.column("description", width=260)
        self.task_table.column("due_date", width=120, anchor="center")
        self.task_table.column("priority", width=90, anchor="center")
        self.task_table.column("status", width=110, anchor="center")
        self.task_table.pack(side="left", fill="both", expand=True)
        self.task_table.bind("<<TreeviewSelect>>", self.select_task)

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.task_table.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.task_table.configure(yscrollcommand=scrollbar.set)

        buttons = ttk.Frame(page)
        buttons.pack(fill="x", pady=(14, 0))
        ttk.Button(
            buttons, text="Mark completed", command=self.mark_completed
        ).pack(side="left")
        ttk.Button(buttons, text="Delete task", command=self.remove_task).pack(
            side="left", padx=8
        )
        ttk.Button(buttons, text="Refresh", command=self.refresh_tasks).pack(side="right")

    def refresh_tasks(self):
        try:
            tasks = database.get_tasks(self.search_entry.get().strip(), self.status_choice.get())
            for item in self.task_table.get_children():
                self.task_table.delete(item)
            for task_id, title, description, due_date, priority, status in tasks:
                self.task_table.insert(
                    "",
                    "end",
                    values=(task_id, title, description or "", due_date or "", priority, status),
                )
            self.selected_task_id = None
        except Exception as error:
            messagebox.showerror("Database error", str(error))

    def select_task(self, event=None):
        selection = self.task_table.selection()
        if selection:
            self.selected_task_id = int(self.task_table.item(selection[0], "values")[0])
        else:
            self.selected_task_id = None

    def add_task(self):
        title = self.title_entry.get().strip()
        description = self.description_entry.get().strip() or None
        due_date = self.date_entry.get().strip()
        if due_date == "YYYY-MM-DD":
            due_date = ""

        if not title:
            messagebox.showwarning("Missing title", "Please enter a task title.")
            return

        try:
            database.add_task(title, description, due_date or None, self.priority_choice.get())
            self.title_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.priority_choice.set("Normal")
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, "YYYY-MM-DD")
            self.refresh_tasks()
        except Exception as error:
            messagebox.showerror("Could not add task", str(error))

    def mark_completed(self):
        if self.selected_task_id is None:
            messagebox.showinfo("Select a task", "Select a task from the list first.")
            return
        try:
            database.complete_task(self.selected_task_id)
            self.refresh_tasks()
        except Exception as error:
            messagebox.showerror("Could not update task", str(error))

    def remove_task(self):
        if self.selected_task_id is None:
            messagebox.showinfo("Select a task", "Select a task from the list first.")
            return
        if not messagebox.askyesno("Delete task", "Delete the selected task?"):
            return
        try:
            database.delete_task(self.selected_task_id)
            self.refresh_tasks()
        except Exception as error:
            messagebox.showerror("Could not delete task", str(error))


def main():
    try:
        database.create_table()
    except Exception as error:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "MySQL connection failed",
            "Check that MySQL is running, the database exists, and task_manager/db_config.py has the correct login.\n\n"
            + str(error),
        )
        root.destroy()
        return

    root = tk.Tk()
    TaskManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
