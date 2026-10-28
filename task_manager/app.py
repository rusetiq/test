from datetime import date
import tkinter as tk
from tkinter import messagebox, ttk

import database
from calendar_picker import CalendarPicker


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskNest")
        self.root.geometry("1020x740")
        self.root.minsize(800, 620)
        self.selected_task_id = None
        self.date_value = tk.StringVar()
        self.setup_style()
        self.build_screen()
        self.refresh_tasks()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        self.root.configure(background="#f1f3ee")
        style.configure("TFrame", background="#f1f3ee")
        style.configure("Surface.TFrame", background="#ffffff")
        style.configure("TLabel", background="#f1f3ee", foreground="#26372d",
                        font=("Arial", 10))
        style.configure("Brand.TLabel", font=("Arial", 14, "bold"), foreground="#285643")
        style.configure("Title.TLabel", font=("Arial", 23, "bold"), foreground="#1d2e24")
        style.configure("Section.TLabel", font=("Arial", 15, "bold"), foreground="#1d2e24")
        style.configure("Muted.TLabel", font=("Arial", 10), foreground="#6a786e")
        style.configure("Surface.TLabel", background="#ffffff", foreground="#26372d",
                        font=("Arial", 10, "bold"))
        style.configure("SurfaceMuted.TLabel", background="#ffffff", foreground="#758278",
                        font=("Arial", 9))
        style.configure("CalendarTitle.TLabel", background="#ffffff", foreground="#26372d",
                        font=("Arial", 11, "bold"))
        style.configure("CalendarWeekday.TLabel", background="#ffffff", foreground="#758278",
                        font=("Arial", 9, "bold"))
        style.configure("TEntry", padding=8, fieldbackground="#ffffff", bordercolor="#d5ddd5",
                        lightcolor="#d5ddd5", darkcolor="#d5ddd5")
        style.configure("TCombobox", padding=7, fieldbackground="#ffffff", bordercolor="#d5ddd5")
        style.map("TCombobox", fieldbackground=[("readonly", "#ffffff")],
                  selectbackground=[("readonly", "#ffffff")],
                  selectforeground=[("readonly", "#26372d")])
        style.configure("TButton", font=("Arial", 10), padding=(12, 8),
                        background="#ffffff", foreground="#26372d", bordercolor="#d5ddd5")
        style.map("TButton", background=[("active", "#e8eee8")])
        style.configure("Accent.TButton", background="#315f4b", foreground="#ffffff",
                        bordercolor="#315f4b", font=("Arial", 10, "bold"))
        style.map("Accent.TButton", background=[("active", "#254a39")],
                  foreground=[("active", "#ffffff")])
        style.configure("Day.TButton", padding=5, background="#ffffff", borderwidth=0)
        style.configure("SelectedDay.TButton", padding=5, background="#315f4b",
                        foreground="#ffffff", borderwidth=0)
        style.map("SelectedDay.TButton", background=[("active", "#254a39")],
                  foreground=[("active", "#ffffff")])
        style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff",
                        foreground="#26372d", rowheight=36, font=("Arial", 10), borderwidth=0)
        style.configure("Treeview.Heading", font=("Arial", 9, "bold"),
                        background="#e7ece5", foreground="#4a5e50", padding=9)
        style.map("Treeview", background=[("selected", "#d5e5d8")],
                  foreground=[("selected", "#1d2e24")])

    def build_screen(self):
        page = ttk.Frame(self.root, padding=(28, 22))
        page.pack(fill="both", expand=True)

        header = ttk.Frame(page)
        header.pack(fill="x")
        ttk.Label(header, text="TaskNest", style="Brand.TLabel").pack(side="left")
        ttk.Label(header, text=date.today().strftime("%A, %d %B %Y"),
                  style="Muted.TLabel").pack(side="right")
        ttk.Separator(page).pack(fill="x", pady=(14, 20))
        ttk.Label(page, text="Your task list", style="Title.TLabel").pack(anchor="w")
        ttk.Label(page, text="Keep your work, due dates and priorities in one place.",
                  style="Muted.TLabel").pack(anchor="w", pady=(5, 18))

        form = ttk.Frame(page, style="Surface.TFrame", padding=18)
        form.pack(fill="x")
        form.columnconfigure(0, weight=3)
        form.columnconfigure(1, weight=2)
        form.columnconfigure(2, weight=1)
        ttk.Label(form, text="NEW TASK", style="SurfaceMuted.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 12))
        ttk.Label(form, text="Task title", style="Surface.TLabel").grid(row=1, column=0, sticky="w")
        ttk.Label(form, text="Description", style="Surface.TLabel").grid(row=1, column=1, sticky="w")
        self.title_entry = ttk.Entry(form)
        self.title_entry.grid(row=2, column=0, sticky="ew", padx=(0, 14), pady=(5, 14))
        self.description_entry = ttk.Entry(form)
        self.description_entry.grid(row=2, column=1, columnspan=2, sticky="ew", pady=(5, 14))
        ttk.Label(form, text="Due date", style="Surface.TLabel").grid(row=3, column=0, sticky="w")
        ttk.Label(form, text="Priority", style="Surface.TLabel").grid(row=3, column=1, sticky="w")
        date_frame = ttk.Frame(form, style="Surface.TFrame")
        date_frame.grid(row=4, column=0, sticky="ew", padx=(0, 14), pady=(5, 0))
        date_frame.columnconfigure(0, weight=1)
        self.date_entry = ttk.Entry(date_frame, textvariable=self.date_value, state="readonly")
        self.date_entry.grid(row=0, column=0, sticky="ew")
        ttk.Button(date_frame, text="Calendar", command=self.open_calendar).grid(
            row=0, column=1, padx=(8, 0))
        self.priority_choice = ttk.Combobox(form, values=("Low", "Normal", "High"),
                                            state="readonly")
        self.priority_choice.grid(row=4, column=1, sticky="ew", padx=(0, 14), pady=(5, 0))
        self.priority_choice.set("Normal")
        ttk.Button(form, text="Add task", style="Accent.TButton", command=self.add_task).grid(
            row=4, column=2, sticky="ew", pady=(5, 0))

        list_heading = ttk.Frame(page)
        list_heading.pack(fill="x", pady=(22, 12))
        ttk.Label(list_heading, text="Tasks", style="Section.TLabel").pack(side="left")
        self.count_label = ttk.Label(list_heading, text="", style="Muted.TLabel")
        self.count_label.pack(side="right")

        filters = ttk.Frame(page)
        filters.pack(fill="x", pady=(0, 10))
        self.search_entry = ttk.Entry(filters, width=30)
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh_tasks())
        ttk.Label(filters, text="Status").pack(side="left", padx=(14, 6))
        self.status_choice = ttk.Combobox(filters, values=("All", "Pending", "Completed"),
                                           state="readonly", width=12)
        self.status_choice.set("All")
        self.status_choice.pack(side="left")
        self.status_choice.bind("<<ComboboxSelected>>", lambda event: self.refresh_tasks())
        ttk.Button(filters, text="Search", command=self.refresh_tasks).pack(side="left", padx=(8, 0))

        table_frame = ttk.Frame(page)
        table_frame.pack(fill="both", expand=True)
        columns = ("id", "title", "description", "due_date", "priority", "status")
        self.task_table = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        headings = ("ID", "TASK", "DESCRIPTION", "DUE DATE", "PRIORITY", "STATUS")
        widths = (45, 180, 230, 110, 90, 110)
        for column, heading, width in zip(columns, headings, widths):
            self.task_table.heading(column, text=heading)
            self.task_table.column(column, width=width, minwidth=40,
                                   anchor="center" if column in ("id", "due_date", "priority", "status") else "w")
        self.task_table.pack(side="left", fill="both", expand=True)
        self.task_table.bind("<<TreeviewSelect>>", self.select_task)
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.task_table.yview)
        scrollbar.pack(side="right", fill="y")
        self.task_table.configure(yscrollcommand=scrollbar.set)
        self.empty_label = ttk.Label(page, text="", style="Muted.TLabel")
        self.empty_label.pack(anchor="w", pady=(6, 0))

        actions = ttk.Frame(page)
        actions.pack(fill="x", pady=(12, 0))
        ttk.Button(actions, text="Mark completed", command=self.mark_completed).pack(side="left")
        ttk.Button(actions, text="Delete task", command=self.remove_task).pack(side="left", padx=8)
        ttk.Button(actions, text="Refresh", command=self.refresh_tasks).pack(side="right")

    def open_calendar(self):
        CalendarPicker(self.root, self.date_value.get(), self.date_value.set)

    def refresh_tasks(self):
        try:
            tasks = database.get_tasks(self.search_entry.get().strip(), self.status_choice.get())
            for item in self.task_table.get_children():
                self.task_table.delete(item)
            for task_id, title, description, due_date, priority, status in tasks:
                self.task_table.insert("", "end", values=(task_id, title, description or "",
                                                          due_date or "", priority, status))
            self.count_label.configure(text=f"{len(tasks)} shown")
            self.empty_label.configure(text="No tasks found. Add a task or change the filters." if not tasks else "")
            self.selected_task_id = None
        except Exception as error:
            messagebox.showerror("Database error", str(error))

    def select_task(self, event=None):
        selection = self.task_table.selection()
        self.selected_task_id = int(self.task_table.item(selection[0], "values")[0]) if selection else None

    def add_task(self):
        title = self.title_entry.get().strip()
        description = self.description_entry.get().strip() or None
        if not title:
            messagebox.showwarning("Missing title", "Please enter a task title.")
            self.title_entry.focus_set()
            return
        try:
            database.add_task(title, description, self.date_value.get() or None, self.priority_choice.get())
            self.title_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.priority_choice.set("Normal")
            self.date_value.set("")
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
