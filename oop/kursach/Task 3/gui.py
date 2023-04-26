from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
from tksheet import Sheet

from db import Database
from student import Student


class GUI:
    def __init__(self, db: Database):
        self.db = db
        self.root = tk.Tk()
        self.raw_data = self.db.get_data()
        self.raw_sheet = None
        self.search_sheet = None
        self.columns_width = (210, 100, 30, 30, 30, 30, 30)
        self.statusbar = tk.Label(self.root, width=20, height=3)
        self.sort_list = [("По умолчанию", "default"), ("[Фамилия] В алфавитном порядке", "name_inc"),
                          ("[Фамилия] В обратном алфавитном порядке", "name_dec"),
                          ("[Группа] По возрастанию", "group_inc"), ("[Группа] По убыванию", "group_dec")]
        self.current_sorting = tk.StringVar(value=self.sort_list[0][0])

    @staticmethod
    def center_window(window):
        window.update_idletasks()
        width = window.winfo_reqwidth()
        height = window.winfo_reqheight()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def update_statusbar(self, text: str):
        text = text[:70] + "..." if len(text) >= 70 else text
        self.statusbar.config(text=text)

    def update_raw_sheet(self):
        sorting = "default"
        for sort_val in self.sort_list:
            if self.current_sorting.get() == sort_val[0]:
                sorting = sort_val[1]
                break
        if sorting == "name_inc":
            self.raw_sheet.set_sheet_data(sorted(self.raw_data, key=lambda x: x[0]))
        elif sorting == "name_dec":
            self.raw_sheet.set_sheet_data(sorted(self.raw_data, key=lambda x: x[0], reverse=True))
        elif sorting == "group_inc":
            self.raw_sheet.set_sheet_data(sorted(self.raw_data, key=lambda x: x[1]))
        elif sorting == "group_dec":
            self.raw_sheet.set_sheet_data(sorted(self.raw_data, key=lambda x: x[1], reverse=True))
        else:
            self.raw_sheet.set_sheet_data(self.raw_data)
        for i, width in enumerate(self.columns_width):
            self.raw_sheet.column_width(column=i, width=width)

    def main_window(self):
        def search_submit():
            search_entry.get()

        self.root.title("Student Records")
        self.root.iconbitmap('../img/people.ico')

        sheet_headers = ['Фамилия, инициалы', 'Группа', '1', '2', '3', '4', '5']
        sheet_width = 520

        raw_table = ttk.Frame(borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        # raw_table.grid_columnconfigure(0, weight=1)
        # raw_table.grid_rowconfigure(0, weight=1)
        self.raw_sheet = Sheet(raw_table, width=sheet_width, height=300, headers=sheet_headers)
        self.update_raw_sheet()
        self.raw_sheet.enable_bindings()
        raw_table.grid(row=0, column=0, padx=5, pady=5)
        self.raw_sheet.grid(row=0, column=0)

        raw_actions = ttk.Frame(borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        ttk.Button(raw_actions, text="Добавить", command=self.add_student_window).pack()
        ttk.Button(raw_actions, text="Удалить", command=self.delete_student_window).pack()
        ttk.Button(raw_actions, text="Сохранить", command=self.save_window).pack()
        ttk.Button(raw_actions, text="Открыть", command=self.open_window).pack()
        ttk.Button(raw_actions, text="Сортировать", command=self.sort_window).pack()
        raw_actions.grid(row=0, column=1, padx=5, pady=5)

        search_table = ttk.Frame(borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        self.search_sheet = Sheet(search_table, width=sheet_width, height=100, headers=sheet_headers)
        self.search_sheet.enable_bindings()
        search_table.grid(row=1, column=0, padx=5, pady=5)
        self.search_sheet.grid(row=0, column=0)

        search_actions = ttk.Frame(borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        search_entry = ttk.Entry(search_actions)
        search_entry.pack()
        ttk.Button(search_actions, text="Поиск", command=search_submit).pack()
        search_actions.grid(row=1, column=1, padx=5, pady=5)

        self.update_statusbar("Готов к работе!")
        self.statusbar.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.center_window(self.root)

        return self.root

    def add_student_window(self):
        def submit(name_field, group_field, grades_fields):
            # TODO: искать совпадения фамилии, убирать точки, проблемы, и сравнивать такие строки
            try:
                student = Student(name_field.get(), group_field.get(), [grade.get() for grade in grades_fields])
            except Exception as err:
                messagebox.showerror("Ошибка", str(err), parent=window)
                return
            else:
                self.raw_data.append([student.name, student.group_number, student.grades[0], student.grades[1],
                                      student.grades[2], student.grades[3], student.grades[4]])
                self.update_raw_sheet()
                self.update_statusbar(f"Добавлена запись: студент {student.name}")
                window.destroy()

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

        ttk.Button(frame, text="Добавить", command=lambda: submit(name, group, grades)).grid(column=1, row=7, sticky=tk.E)

        frame.grid(column=0, row=0)
        self.center_window(window)

    def delete_student_window(self):
        selection = self.raw_sheet.get_selected_rows(get_cells=False, get_cells_as_rows=True, return_tuple=False)
        if not selection:
            self.update_statusbar("Выделите ячейки (строки) для удаления записей")
        else:
            result = messagebox.askyesno(title="Подтвердите удаление",
                                         message="Вы действительно хотите удалить информацию о следующих студентах:\n" +
                                                 "\n".join([self.raw_data[record][0] for record in selection]))
            if result:
                for record in sorted(selection, reverse=True):
                    del self.raw_data[record]
                self.update_raw_sheet()
                self.update_statusbar("Удалены записи о студентах: " + "\n".join([self.raw_data[record][0] for record in selection]))
            else:
                return

    def save_window(self):
        if self.raw_data == self.db.get_data():
            self.update_statusbar('Данные не изменены, сохранять не требуется')
            return
        result = messagebox.askyesno(title="Сохранить изменения?",
                                     message="Вы действительно хотите перезаписать информацию в файле?")
        if result:
            self.db.update_data(self.raw_data)
            self.update_statusbar("Успешно сохранено!")
        else:
            return

    def open_window(self):
        filetypes = (
            ('SQLite database', '*.db'),
            ('SQLite database', '*.sqlite3'),
        )
        filename = filedialog.askopenfilename(title='Открыть базу данных', initialdir=Path(__file__).parent.resolve(),
                                              filetypes=filetypes)
        if not filename:
            return
        try:
            db_new = Database(filename)
            db_new.start()
            raw_data_new = db_new.get_data()
        except Exception:
            messagebox.showerror("Ошибка открытия файла", "Ошибка при открытии базы данных.", parent=self.root)
        else:
            self.db.stop()
            self.db = db_new
            self.raw_data = raw_data_new
            self.update_raw_sheet()
            self.update_statusbar(f"Открыта база данных: {filename}")

    def sort_window(self):
        def submit():
            selection = self.current_sorting.get()
            self.update_statusbar("Сортировка по: {}".format(selection))
            self.update_raw_sheet()
            window.destroy()

        window = tk.Toplevel()
        window.title("Сортировка")

        frame = ttk.Frame(window, padding=[20, 20])

        ttk.Label(frame, text='Сортировка').grid(column=0, row=0, sticky=tk.W)

        sorting = ttk.Combobox(frame, values=[sort_val[0] for sort_val in self.sort_list], textvariable=self.current_sorting, state="readonly",
                               width=40)
        sorting.grid(column=0, row=1, sticky=tk.W)

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)

        ttk.Button(frame, text="Применить", command=submit).grid(column=0, row=2, sticky=tk.E)

        frame.grid(column=0, row=0)
        self.center_window(window)
