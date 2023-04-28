from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
from tksheet import Sheet

from db import LocalMemory
from student import Student


class GUI:
    def __init__(self):
        self.memory = LocalMemory('students.db')
        self.root = tk.Tk()
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

    def sort_data(self, data):
        sorting = "default"
        for sort_val in self.sort_list:
            if self.current_sorting.get() == sort_val[0]:
                sorting = sort_val[1]
                break
        if sorting == "name_inc":
            return sorted(data, key=lambda x: x[0])
        elif sorting == "name_dec":
            return sorted(data, key=lambda x: x[0], reverse=True)
        elif sorting == "group_inc":
            return sorted(data, key=lambda x: x[1])
        elif sorting == "group_dec":
            return sorted(data, key=lambda x: x[1], reverse=True)
        else:
            return data

    def update_raw_sheet(self):
        self.raw_sheet.set_sheet_data(self.sort_data(self.memory.data))
        for i, width in enumerate(self.columns_width):
            self.raw_sheet.column_width(column=i, width=width)

    def main_window(self):
        def search_submit():
            phrase = search_entry.get()
            if not phrase:
                self.update_statusbar("Поисковая фраза пуста.")
                return
            results = self.memory.search(phrase)
            self.search_sheet.set_sheet_data(self.sort_data(results))
            for i, width in enumerate(self.columns_width):
                self.search_sheet.column_width(column=i, width=width)

        def without_scholarship():
            results = self.memory.search_without_scholarship()
            self.search_sheet.set_sheet_data(self.sort_data(results))
            for i, width in enumerate(self.columns_width):
                self.search_sheet.column_width(column=i, width=width)

        def on_closing():
            if self.memory.is_changed:
                if messagebox.askokcancel("Выход", "Есть несохраненные изменения. Вы уверены, что хотите выйти без сохранения?"):
                    self.root.destroy()
            else:
                self.root.destroy()

        self.root.title("Студенты")
        self.root.iconbitmap('../img/people.ico')
        self.root.protocol("WM_DELETE_WINDOW", on_closing)

        button_sizes = {'ipadx': 20, 'ipady': 5}
        sheet_headers = ['Фамилия, инициалы', 'Группа', '1', '2', '3', '4', '5']
        sheet_width = 520

        self.root.option_add("*tearOff", tk.FALSE)
        main_menu = tk.Menu()
        file_menu = tk.Menu()
        file_menu.add_command(label="Создать", command=self.create_window)
        file_menu.add_command(label="Открыть", command=self.open_window)
        file_menu.add_command(label="Сохранить", command=self.save_window)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=on_closing)
        edit_menu = tk.Menu()
        edit_menu.add_command(label="Добавить", command=self.add_student_window)
        edit_menu.add_command(label="Удалить", command=self.delete_student_window)
        view_menu = tk.Menu()
        view_menu.add_command(label="Обновить", command=self.update_raw_sheet)
        view_menu.add_command(label="Сортировать", command=self.sort_window)
        info_menu = tk.Menu()
        info_menu.add_command(label="О разработчике", command=self.about_developer_window)
        main_menu.add_cascade(label="Файл", menu=file_menu)
        main_menu.add_cascade(label="Редактировать", menu=edit_menu)
        main_menu.add_cascade(label="Просмотр", menu=view_menu)
        main_menu.add_cascade(label="Справка", menu=info_menu)
        self.root.config(menu=main_menu)

        raw_table = ttk.Frame(borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        # raw_table.grid_columnconfigure(0, weight=1)
        # raw_table.grid_rowconfigure(0, weight=1)
        self.raw_sheet = Sheet(raw_table, width=sheet_width, height=300, headers=sheet_headers)
        self.update_raw_sheet()
        self.raw_sheet.enable_bindings()
        raw_table.grid(row=0, column=0, padx=5, pady=5)
        self.raw_sheet.grid(row=0, column=0)

        raw_actions = ttk.Frame(borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        ttk.Label(raw_actions, text="").pack(ipady=20)
        ttk.Button(raw_actions, text="Добавить", command=self.add_student_window, width=10).pack(**button_sizes)
        ttk.Button(raw_actions, text="Удалить", command=self.delete_student_window, width=10).pack(**button_sizes)
        ttk.Button(raw_actions, text="Сохранить", command=self.save_window, width=10).pack(**button_sizes)
        ttk.Button(raw_actions, text="Открыть", command=self.open_window, width=10).pack(**button_sizes)
        ttk.Button(raw_actions, text="Сортировать", command=self.sort_window, width=10).pack(**button_sizes)
        raw_actions.grid(row=0, column=1, padx=5, pady=5, sticky="NSWE")

        search_table = ttk.Frame(borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        self.search_sheet = Sheet(search_table, width=sheet_width, height=100, headers=sheet_headers)
        for i, width in enumerate(self.columns_width):
            self.search_sheet.column_width(column=i, width=width)
        self.search_sheet.enable_bindings()
        search_table.grid(row=1, column=0, padx=5, pady=5)
        self.search_sheet.grid(row=0, column=0)

        search_actions = ttk.Frame(borderwidth=1, relief=tk.SOLID, padding=[8, 10])
        search_entry = ttk.Entry(search_actions)
        search_entry.pack(pady=3)
        ttk.Button(search_actions, text="Поиск", command=search_submit, width=10).pack(**button_sizes)
        ttk.Button(search_actions, text="Без стипендии", command=without_scholarship, width=10).pack(**button_sizes)
        search_actions.grid(row=1, column=1, padx=5, pady=5, sticky="NSWE")

        self.update_statusbar("Готов к работе! Открыта база данных: students.db")
        self.statusbar.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.center_window(self.root)

        return self.root

    def add_student_window(self):
        def submit(name_field, group_field, grades_fields):
            try:
                student = Student(name_field.get(), group_field.get(), [grade.get() for grade in grades_fields])
            except Exception as err:
                messagebox.showerror("Ошибка", str(err), parent=window)
                return
            else:
                results = self.memory.search(student.name, only_name=True)
                if results:
                    is_save = messagebox.askyesno(title="Найдено совпадение",
                                                  message="В базе данных уже есть сведения о следующих студентах:\n" +
                                                  "\n".join(["{}, {}".format(result[0], result[1]) for result in results]) +
                                                          "\nПродолжить добавление студента?", parent=window)
                    if not is_save:
                        return
                self.memory.add_student(student)
                self.update_raw_sheet()
                self.update_statusbar(f"Добавлен студент {student.name}")
                window.destroy()

        window = tk.Toplevel()
        window.title("Добавление студента")

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
                                                 "\n".join(["{}, {}".format(self.memory.data[record][0], self.memory.data[record][1]) for record in selection]))
            if result:
                self.update_statusbar("Удалены записи о студентах: " + ", ".join(["{}".format(self.memory.data[record][0]) for record in selection]))
                self.memory.delete_students(selection)
                self.update_raw_sheet()
            else:
                return

    def save_window(self):
        def submit():
            is_error, message = self.memory.save(file_entry.get())
            if is_error:
                messagebox.showerror('Ошибка', message)
            else:
                self.update_statusbar(message)
            window.destroy()

        window = tk.Toplevel()
        window.title("Сохранение")

        frame = ttk.Frame(window, padding=[20, 20])

        ttk.Label(frame, text='Название файла').grid(column=0, row=0, sticky=tk.W)

        file_entry = ttk.Entry(frame, width=40)
        file_entry.insert(0, self.memory.db_name)
        file_entry.focus()
        file_entry.grid(column=0, row=1, sticky=tk.W)

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)

        ttk.Button(frame, text="Сохранить", command=submit).grid(column=0, row=2, sticky=tk.E)

        frame.grid(column=0, row=0)
        self.center_window(window)

    def open_window(self):
        filetypes = (
            ('SQLite database', '*.db'),
            ('SQLite database', '*.sqlite3'),
        )
        filepath = filedialog.askopenfilename(title='Открыть базу данных', initialdir=Path(__file__).parent.resolve(),
                                              filetypes=filetypes)
        if not filepath:
            return
        is_error, message = self.memory.open(filepath)
        if is_error:
            messagebox.showerror("Ошибка открытия файла", message, parent=self.root)
        else:
            self.update_raw_sheet()
            self.update_statusbar(message)

    def create_window(self):
        def submit():
            is_error, message = self.memory.open(file_entry.get())
            if is_error:
                messagebox.showerror('Ошибка', message, parent=window)
                return
            else:
                self.update_raw_sheet()
                self.update_statusbar(message)
            window.destroy()

        window = tk.Toplevel()
        window.title("Создание базы данных")

        frame = ttk.Frame(window, padding=[20, 20])

        ttk.Label(frame, text='Текущая директория: {}'.format(Path(__file__).parent.resolve())).grid(column=0, row=0, sticky=tk.W)
        ttk.Label(frame, text='Название файла:').grid(column=0, row=1, sticky=tk.W)
        file_entry = ttk.Entry(frame, width=40)
        file_entry.insert(0, '.db')
        file_entry.focus()
        file_entry.grid(column=0, row=2, sticky=tk.W)

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)

        ttk.Button(frame, text="Создать", command=submit).grid(column=0, row=3, sticky=tk.E)

        frame.grid(column=0, row=0)
        self.center_window(window)

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

    def about_developer_window(self):
        def open_github():
            from webbrowser import open_new
            open_new("https://github.com/maks-burlakof/university/")

        window = tk.Toplevel()
        window.title("О разработчике")

        frame = ttk.Frame(window, padding=[20, 20])

        ttk.Label(frame, text='Курсовой проект ООПвСУ, 3 часть\nРазработал: Бурлаков Максим, гр. 122402').grid(column=0, row=0, sticky=tk.W)
        ttk.Button(frame, text='Исходный код на GitHub', cursor="hand2", command=open_github).grid(column=0, row=1, sticky=tk.W, ipady=1)

        frame.grid(column=0, row=0)
        self.center_window(window)
