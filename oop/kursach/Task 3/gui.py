import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tksheet import Sheet

from db import Database
from student import Student


class GUI:
    def __init__(self, db: Database):
        self.db = db
        self.root = tk.Tk()
        self.root.title("Student Records")
        self.root.iconbitmap('../img/people.ico')
        self.root.geometry('900x600')

    def main_window(self):
        raw_table = ttk.Frame(borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        raw_table.grid_columnconfigure(0, weight=1)
        raw_table.grid_rowconfigure(0, weight=1)
        sheet = Sheet(raw_table, data=[[f"Row {r}, Column {c}\nnewline1\nnewline2" for c in range(50)] for r in range(500)])
        sheet.enable_bindings()
        raw_table.grid(row=0, column=0, padx=5, pady=5)
        sheet.grid(row=0, column=0)

        raw_actions = ttk.Frame(borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        ttk.Button(raw_actions, text="Добавить", command=self.add_student_window).pack()
        ttk.Button(raw_actions, text="Удалить").pack()
        ttk.Button(raw_actions, text="Сохранить").pack()
        ttk.Button(raw_actions, text="Открыть").pack()
        ttk.Button(raw_actions, text="Сортировать").pack()
        raw_actions.grid(row=0, column=1, padx=5, pady=5)

        result_table = ttk.Frame(borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        ttk.Label(result_table, text="Результаты поиска").pack(anchor=tk.NW)
        ttk.Entry(result_table).pack(anchor=tk.NW)
        result_table.grid(row=1, column=0, padx=5, pady=5)

        result_actions = ttk.Frame(borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        ttk.Entry(result_actions).pack()
        ttk.Button(result_actions, text="Поиск").pack()
        result_actions.grid(row=1, column=1, padx=5, pady=5)

        return self.root

    def add_student_window(self):
        window = tk.Toplevel()
        window.title("Добавление записи")

        frame = ttk.Frame(window, padding=[20, 20])
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(0, weight=3)

        ttk.Label(frame, text='Фамилия и инициалы:').grid(column=0, row=0, sticky=tk.W)
        name = ttk.Entry(frame, width=30)
        name.focus()
        name.grid(column=1, row=0, sticky=tk.W)

        ttk.Label(frame, text='Номер группы:').grid(column=0, row=1, sticky=tk.W)
        group = ttk.Entry(frame, width=30)
        group.grid(column=1, row=1, sticky=tk.W)

        ttk.Label(frame, text='Успеваемость:').grid(column=0, row=2, sticky=tk.W)
        grades = []
        for i in range(2, 7):
            grades.append(ttk.Entry(frame, width=6))
            grades[-1].grid(column=1, row=i, sticky=tk.W)

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)

        ttk.Button(frame, text="Добавить", command=lambda: self.add_student_submit(window, name, group, grades)).grid(column=1, row=7, sticky=tk.E)

        frame.grid(column=0, row=0)

    def add_student_submit(self, window, name_field, group_field, grades_fields):
        # TODO: искать совпадения фамилии, убирать точки, проблемы, и сравнивать такие строки
        try:
            student = Student(name_field.get(), group_field.get(), [grade.get() for grade in grades_fields])
        except Exception as err:
            messagebox.showerror("Ошибка", str(err), parent=window)
            return
        else:
            self.db.add_student(student)
            window.destroy()

    def view_students_window(self):
        pass
