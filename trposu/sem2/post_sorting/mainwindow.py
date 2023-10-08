from tkinter import *
from tkinter import ttk, messagebox
import functools
from localmemory import LocalMemory


class Window(Tk):
    def __init__(self, memory: LocalMemory):
        super().__init__()
        self.memory = memory

        self.base_title = 'Сортировка посылок международной почты'
        self.title(self.base_title)
        self.favicon_path = 'assets/favicon.ico'
        self.iconbitmap(self.favicon_path)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.option_add("*tearOff", FALSE)
        main_menu = Menu()
        file_menu = Menu()
        file_menu.add_command(label="Сохранить", command=self.save)
        file_menu.add_command(label="Закрыть", command=self.on_closing)
        main_menu.add_cascade(label="Файл", menu=file_menu)
        view_menu = Menu()
        view_menu.add_command(label="Меню 1", command=self.show_menu_1)
        view_menu.add_command(label="Меню 2", command=self.show_menu_2)
        view_menu.add_command(label="Меню 3", command=self.show_menu_3)
        main_menu.add_cascade(label="Просмотр", menu=view_menu)
        main_menu.add_cascade(label="Аккаунт", command=self.show_login)
        self.config(menu=main_menu)

        tabs = ttk.Frame()
        tabs.grid(row=0, column=0, padx=5, pady=10, sticky='N')
        tabs_sizes = {'ipadx': 20, 'ipady': 5, 'padx': 5, 'row': 1}
        ttk.Button(tabs, text="Меню 1", command=self.show_menu_1, width=10).grid(**tabs_sizes, column=0)
        ttk.Button(tabs, text="Меню 2", command=self.show_menu_2, width=10).grid(**tabs_sizes, column=1)
        ttk.Button(tabs, text="Меню 3", command=self.show_menu_3, width=10).grid(**tabs_sizes, column=2)

        self.statusbar = ttk.Label(self, text=f'Готов к работе! Открыта база данных: {self.memory.db_name}')
        self.statusbar.grid(row=2, column=0, pady=3)

        self.btns_sizes = {'ipady': 5, 'ipadx': 5}

        self.center_window(self, 800, 500)
        self.show_login()

    @staticmethod
    def center_window(window, width: int = None, height: int = None):
        window.update_idletasks()
        width = width or window.winfo_reqwidth()
        height = height or window.winfo_reqheight()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def update_statusbar(self, text: str):
        text = text[:70] + "..." if len(text) >= 70 else text
        self.statusbar.config(text=text)

    def show_content(integrate: str = '', title: str = ''):
        def decorator(window_func):
            @functools.wraps(window_func)
            def embed_wrapper(self):
                self.title(title + ' - ' + self.base_title)
                window = ttk.Frame()
                window = window_func(self, window)
                window.grid(row=1, column=0, padx=10, pady=5, sticky='NSWE')

            @functools.wraps(window_func)
            def separate_wrapper(self):
                window = Toplevel()
                window.iconbitmap(self.favicon_path)
                window.title(title)
                window = window_func(self, window)
                self.center_window(window)
            if integrate == 'embed':
                return embed_wrapper
            elif integrate == 'separate':
                return separate_wrapper
        return decorator

    @show_content(integrate='embed', title='Войти')
    def show_login(self, window):
        def submit():
            if login_entry.get() and password_entry.get() and self.memory.validate_login(login_entry.get(), password_entry.get()):
                self.update_statusbar(f'Выполнен вход в аккаунт @{self.memory.authenticated_user}')
                self.show_account()
            else:
                error_label['text'] = 'Неверное имя пользователя или пароль.'

        if self.memory.authenticated_user:
            self.show_account()

        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)

        form_frame = ttk.Frame(window)
        form_frame.grid(row=0, column=0)

        login_frame = ttk.Frame(form_frame)
        login_frame.pack(pady=2)
        ttk.Label(login_frame, text='Логин').pack(anchor='w', pady=5)
        login_entry = ttk.Entry(login_frame, width=42)
        login_entry.pack(ipady=4)
        login_entry.focus()

        password_frame = ttk.Frame(form_frame)
        password_frame.pack(pady=2)
        ttk.Label(password_frame, text='Пароль').pack(anchor='w', pady=5)
        password_entry = ttk.Entry(password_frame, show='*', width=42)
        password_entry.pack(ipady=4)

        ttk.Button(form_frame, text="Войти", command=submit, width=40).pack(**self.btns_sizes, pady=15)

        error_label = ttk.Label(form_frame, text='', foreground='red', width=40)
        error_label.pack(anchor='w')

        return window

    @show_content(integrate='embed', title='Аккаунт')
    def show_account(self, window):
        def logout():
            if messagebox.askyesno('Выйти из аккаунта?', 'Вы действительно хотите выйти из аккаунта?'):
                self.memory.authenticated_user = None
                self.update_statusbar('Выполнен выход из аккаунта')
                self.show_login()

        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)

        frame = ttk.Frame(window)
        frame.grid(row=0, column=0)

        ttk.Label(frame, text=f'Вы вошли как @{self.memory.authenticated_user}').pack(anchor='w', pady=2)
        if self.memory.authenticated_user.permissions == 1:
            ttk.Label(frame, text='Администратор').pack(anchor='w')
        ttk.Button(frame, text="Выйти", command=logout, width=40).pack(**self.btns_sizes, pady=10)

        return window

    @show_content(integrate='embed', title='Меню 1')
    def show_menu_1(self, window):
        def select_office(event):
            office = office_combobox.get()
            streets = self.memory.get_streets_by_office(office)
            street_combobox['values'] = streets
            street_combobox._values = streets
            street_combobox.set('')

        def submit():
            response = self.memory.add_parcel(office_combobox.get(), street_combobox.get())
            if response['success']:
                self.update_statusbar(f"Добавлено: {response['instance']}")
                self.show_menu_1()
            else:
                error_label['text'] = response['message']

        def update_info():
            data_str = '\n'.join(['Отделение №{} - {} шт.'.format(office.number, data['total']) for office, data in self.memory.parcels_info.items()])
            info_label['text'] = 'Информация о посылках:\n\n' + (data_str or 'Посылок нет')

        window.grid_rowconfigure(0, weight=1)
        for c in range(1): window.columnconfigure(index=c, weight=1)

        form_frame = ttk.Frame(window)
        form_frame.grid(row=0, column=0)

        office_frame = ttk.Frame(form_frame)
        office_frame.grid(row=0, column=0, padx=5)
        ttk.Label(office_frame, text="Отделение").pack(anchor='w', pady=5)
        office_combobox = ComboboxObjs(office_frame, values=self.memory.offices, state="readonly", width=27)
        office_combobox.pack(ipady=3)
        office_combobox.bind("<<ComboboxSelected>>", select_office)

        street_frame = ttk.Frame(form_frame)
        street_frame.grid(row=0, column=1)
        ttk.Label(street_frame, text="Улица").pack(anchor='w', pady=5)
        street_combobox = ComboboxObjs(street_frame, values=[], state="readonly", width=27)
        street_combobox.pack(ipady=3)

        error_label = ttk.Label(form_frame, text='', foreground='red')
        error_label.grid(row=1, columnspan=2, sticky='W', padx=5)

        ttk.Button(form_frame, text="Зарегистрировать", command=submit, width=20).grid(**self.btns_sizes, row=2, column=1, sticky='E', pady=2)

        info_frame = ttk.Frame(window, width=500, borderwidth=1, relief=SOLID)
        info_frame.grid(row=0, column=1, padx=30)
        info_label = ttk.Label(info_frame, text='', width=30)
        info_label.pack(ipady=4, ipadx=4)
        update_info()

        return window

    @show_content(integrate='embed', title='Меню 2')
    def show_menu_2(self, window):
        def select_office(event):
            info_template = 'Отделение №{}\n\nПосылок: {} шт.\n- больших: {} шт.\n- средних: {} шт.\n- маленьких: {} шт.'
            try:
                info_label['text'] = next(info_template.format(office.number, data['total'], data['1'], data['2'], data['3']) for office, data in self.memory.parcels_info.items() if office.id == office_combobox.get().id)
            except StopIteration:
                info_label['text'] = 'Отделение №{}\nПосылок нет.'.format(office_combobox.get().number)

        def submit():
            if not street_entry.get():
                street_error['text'] = 'Укажите название улицы'
                street_entry.focus()
                return
            if not selected_type.get():
                street_error['text'] = 'Укажите тип посылки'
                return
            street = self.memory.get_office_street_by_street_name(street_entry.get())
            if street:
                response = self.memory.add_parcel(street.office, street, selected_type.get())
                if response['success']:
                    self.update_statusbar(f"Добавлено: {response['instance']}")
                    self.show_menu_2()
                else:
                    street_error['text'] = response['message']
            else:
                street_error['text'] = 'Такой улицы не существует'
                street_entry.focus()

        window.grid_rowconfigure(0, weight=1)
        for c in range(1): window.columnconfigure(index=c, weight=1)

        form_frame = ttk.Frame(window)
        form_frame.grid(row=0, column=0)

        ttk.Label(form_frame, text='Улица').pack(anchor='w', pady=5)
        street_entry = ttk.Entry(form_frame, width=35)
        street_entry.pack(ipady=4)
        street_entry.focus()
        street_error = ttk.Label(form_frame, text='', foreground='red', width=35)
        street_error.pack(anchor='w', pady=5)

        selected_type = IntVar()
        ttk.Label(form_frame, text='Вид посылки').pack(anchor='w', pady=5)
        type_big_btn = ttk.Radiobutton(form_frame, text='Большая посылка', value=1, variable=selected_type)
        type_big_btn.pack(anchor='w')
        type_mid_btn = ttk.Radiobutton(form_frame, text='Средняя посылка', value=2, variable=selected_type)
        type_mid_btn.pack(anchor='w')
        type_sm_btn = ttk.Radiobutton(form_frame, text='Маленькая посылка', value=3, variable=selected_type)
        type_sm_btn.pack(anchor='w')

        ttk.Button(form_frame, text="Зарегистрировать", command=submit, width=20).pack(**self.btns_sizes, anchor='w', pady=20)

        info_frame = ttk.Frame(window)
        info_frame.grid(row=0, column=1, sticky='W', padx=50)

        ttk.Label(info_frame, text='Отделение').pack(anchor='w', pady=5)
        office_combobox = ComboboxObjs(info_frame, values=self.memory.offices, state="readonly", width=30)
        office_combobox.pack(ipady=4)
        office_combobox.bind("<<ComboboxSelected>>", select_office)

        info_label = ttk.Label(info_frame, text='')
        info_label.pack(anchor='w', pady=20)

        return window

    @show_content(integrate='embed', title='Меню 3')
    def show_menu_3(self, window):
        window.grid_rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)

        btns_frame = ttk.Frame(window)
        btns_frame.grid(row=0, column=0)

        if self.memory.authenticated_user and self.memory.authenticated_user.permissions == 1:
            ttk.Button(btns_frame, text="Добавить отделение", command=self.show_add_office, width=30).pack(**self.btns_sizes, pady=5)
            ttk.Button(btns_frame, text="Добавить улицу", command=self.show_add_street, width=30).pack(**self.btns_sizes, pady=5)
        ttk.Button(btns_frame, text="Состояние отделения", command=self.show_info_office, width=30).pack(**self.btns_sizes, pady=5)

        return window

    @show_content(integrate='separate', title='Добавить отделение')
    def show_add_office(self, window):
        def submit():
            response = self.memory.add_office(office_entry.get())
            if response['success']:
                self.update_statusbar(f"Добавлено отделение №{response['instance'].number}")
                window.destroy()
            else:
                messagebox.showerror('Ошибка', response['message'], parent=window)

        def update_info():
            offices_str = ', '.join([office.number for office in self.memory.offices])
            info_label['text'] = 'Отделения:\n' + (offices_str or 'Отделений нет')

        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)

        form_frame = ttk.Frame(window)
        form_frame.grid(row=0, column=0, pady=15, padx=25)

        ttk.Label(form_frame, text='Номер отделения').pack(anchor='w', pady=5)
        office_entry = ttk.Entry(form_frame, width=60)
        office_entry.pack(ipady=4)

        btns_frame = ttk.Frame(form_frame)
        btns_frame.pack(pady=9, fill='x')
        ttk.Button(btns_frame, text="Подтвердить", command=submit, width=20).pack(**self.btns_sizes, anchor='w', side='left')
        ttk.Button(btns_frame, text="Отменить", command=window.destroy, width=20).pack(**self.btns_sizes, anchor='e', side='right')

        info_label = ttk.Label(form_frame, text='', width=60)
        info_label.pack(ipady=20)
        update_info()

        return window

    @show_content(integrate='separate', title='Добавить улицу')
    def show_add_street(self, window):
        def submit():
            response = self.memory.add_street(street_entry.get(), office_combobox.get())
            if response['success']:
                instance = response['instance']
                self.update_statusbar('Добавлена улица {} к отделению №{}'.format(instance.name, instance.office.number))
                window.destroy()
            else:
                messagebox.showerror('Ошибка', response['message'], parent=window)

        window.rowconfigure(0, weight=1)
        window.columnconfigure(0, weight=1)

        form_frame = ttk.Frame(window)
        form_frame.grid(row=0, column=0, pady=15, padx=30)

        street_frame = ttk.Frame(form_frame)
        street_frame.pack(pady=2)
        ttk.Label(street_frame, text='Название').pack(anchor='w', pady=5)
        street_entry = ttk.Entry(street_frame, width=63)
        street_entry.pack(ipady=4)

        office_frame = ttk.Frame(form_frame)
        office_frame.pack(pady=2)
        ttk.Label(office_frame, text='Отделение').pack(anchor='w', pady=5)
        office_combobox = ComboboxObjs(office_frame, values=self.memory.offices, state="readonly", width=60)
        office_combobox.pack(ipady=4)

        btns_frame = ttk.Frame(form_frame)
        btns_frame.pack(pady=20, fill='x')
        ttk.Button(btns_frame, text="Подтвердить", command=submit, width=20).pack(**self.btns_sizes, anchor='w', side='left')
        ttk.Button(btns_frame, text="Отменить", command=window.destroy, width=20).pack(**self.btns_sizes, anchor='e', side='right')

        return window

    @show_content(integrate='separate', title='Состояние отделения')
    def show_info_office(self, window):
        def select_office(event):
            info_template = 'Отделение №{}\n\nПосылок: {} шт.\n- больших: {} шт.\n- средних: {} шт.\n- маленьких: {} шт.'
            try:
                info_label['text'] = next(info_template.format(office.number, data['total'], data['1'], data['2'], data['3']) for office, data in self.memory.parcels_info.items() if office.id == office_combobox.get().id)
            except StopIteration:
                info_label['text'] = 'Отделение №{}\nПосылок нет.'.format(office_combobox.get().number)
            finally:
                self.center_window(window)

        info_frame = ttk.Frame(window)
        info_frame.grid(row=0, column=0, pady=20, padx=50)

        ttk.Label(info_frame, text='Отделение').pack(anchor='w', pady=5)
        office_combobox = ComboboxObjs(info_frame, values=self.memory.offices, state="readonly", width=50)
        office_combobox.pack(ipady=4)
        office_combobox.bind("<<ComboboxSelected>>", select_office)

        info_label = ttk.Label(info_frame, text='', width=50)
        info_label.pack(anchor='w', pady=20)

        return window

    def save(self):
        is_save = messagebox.askyesno('Сохранить изменения?', 'Вы действительно хотите сохранить в базе данных внесенные изменения?')
        if is_save:
            response = self.memory.save()
            self.update_statusbar(response['message'])

    def on_closing(self):
        if self.memory.is_changed:
            if messagebox.askokcancel('Выход', 'Есть несохраненные изменения. Вы уверены, что хотите выйти без сохранения?'):
                self.destroy()
        else:
            self.destroy()


class ComboboxObjs(ttk.Combobox):
    def __init__(self, *args, values: list = None, **kwargs):
        super().__init__(*args, values=values, **kwargs)
        if values is None:
            values = []
        self._values = values

    def get(self):
        if self.current() == -1:
            return None
        else:
            return self._values[self.current()]
