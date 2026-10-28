import calendar
from datetime import date
import tkinter as tk
from tkinter import ttk


class CalendarPicker:
    def __init__(self, parent, current_value, on_select):
        self.on_select = on_select
        try:
            self.selected_date = date.fromisoformat(current_value)
        except ValueError:
            self.selected_date = None
        current = self.selected_date or date.today()
        self.year = current.year
        self.month = current.month
        self.window = tk.Toplevel(parent)
        self.window.title("Choose a due date")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.bind("<Escape>", lambda event: self.window.destroy())
        self.window.grab_set()
        self.content = ttk.Frame(self.window, padding=18, style="Surface.TFrame")
        self.content.pack(fill="both", expand=True)
        self.draw_month()

    def change_month(self, amount):
        month_number = (self.year - 1) * 12 + self.month - 1 + amount
        if 0 <= month_number < 9999 * 12:
            self.year, month_index = divmod(month_number, 12)
            self.year += 1
            self.month = month_index + 1
            self.draw_month()

    def choose_day(self, day):
        self.on_select(date(self.year, self.month, day).isoformat())
        self.window.destroy()

    def clear_date(self):
        self.on_select("")
        self.window.destroy()

    def draw_month(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        heading = ttk.Frame(self.content, style="Surface.TFrame")
        heading.grid(row=0, column=0, columnspan=7, sticky="ew", pady=(0, 12))
        ttk.Button(heading, text="<", width=3, command=lambda: self.change_month(-1)).pack(side="left")
        ttk.Button(heading, text=">", width=3, command=lambda: self.change_month(1)).pack(side="right")
        ttk.Label(heading, text=f"{calendar.month_name[self.month]} {self.year}",
                  style="CalendarTitle.TLabel").pack(expand=True)
        for index, day_name in enumerate(("M", "T", "W", "T", "F", "S", "S")):
            ttk.Label(self.content, text=day_name, anchor="center",
                      style="CalendarWeekday.TLabel").grid(row=1, column=index, padx=2, pady=(0, 4), sticky="ew")
        for row, week in enumerate(calendar.monthcalendar(self.year, self.month), start=2):
            for column, day in enumerate(week):
                if day:
                    is_selected = self.selected_date == date(self.year, self.month, day)
                    style = "SelectedDay.TButton" if is_selected else "Day.TButton"
                    ttk.Button(self.content, text=str(day), width=3, style=style,
                               command=lambda value=day: self.choose_day(value)).grid(
                        row=row, column=column, padx=2, pady=2, sticky="ew")
        ttk.Button(self.content, text="Clear date", command=self.clear_date).grid(
            row=9, column=0, columnspan=7, sticky="ew", pady=(12, 0))
