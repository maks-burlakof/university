from tkinter import Tk, Label, Entry, Button, messagebox, filedialog
from tkinter.constants import END

from pyautocad import Autocad


class AutoCAD:
    def __new__(cls, *args, **kwargs):
        print('Initialising new AutoCAD system process')
        return super(AutoCAD, cls).__new__(cls)

    def __init__(self):
        self.acad = Autocad(create_if_not_exists=True)
        self.point = [0, 0, 0]
        self.solidity = [32, 32]
        self.filepath = ""
        self.acad.prompt("Hello, Autocad from Python. Document: {}".format(self.acad.doc.Name))

    def set_point_coordinates(self):
        self.acad.doc.SendCommand('_ID ')
        self.point = list(self.acad.doc.GetVariable("LASTPOINT"))
        return self.point

    def set_color(self):
        self.acad.doc.SendCommand('_COLOR \r')


class WindowGUI:
    def __new__(cls, *args, **kwargs):
        print('Started new window process')
        return super(WindowGUI, cls).__new__(cls)

    def __init__(self, acad: AutoCAD):
        self.window = Tk()
        self.acad = acad
        self.set_up = False
        self.x_enter = None
        self.y_enter = None
        self.m_input = None
        self.n_input = None

    def setup(self):
        self.window.title('Edge Surface')
        self.window.geometry('300x400')

        FS_HEADINGS = 12
        FS_INPUTS = 10
        FONT = "Arial Bold"

        Label(self.window, text="Точка вставки", font=(FONT, FS_HEADINGS)).grid(column=0, row=0)
        Label(self.window, text="Координата X: ", font=(FONT, FS_INPUTS)).grid(column=0, row=1)
        self.x_enter = Entry(self.window, width=10)
        self.x_enter.grid(column=1, row=1)
        self.x_enter.insert(0, self.acad.point[0])
        Label(self.window, text="Координата Y: ", font=(FONT, FS_INPUTS)).grid(column=0, row=2)
        self.y_enter = Entry(self.window, width=10)
        self.y_enter.grid(column=1, row=2)
        self.y_enter.insert(0, self.acad.point[1])
        Button(self.window, text="Указать мышью -->", command=self.get_point_coordinates).grid(column=0, row=3)
        Label(self.window, text="Плотность сетки", font=(FONT, FS_HEADINGS)).grid(column=0, row=4)
        Label(self.window, text="M-плотность: ", font=(FONT, FS_INPUTS)).grid(column=0, row=5)
        self.m_input = Entry(self.window, width=5)
        self.m_input.grid(column=1, row=5)
        self.m_input.insert(0, self.acad.solidity[0])
        Label(self.window, text="N-плотность: ", font=(FONT, FS_INPUTS)).grid(column=0, row=6)
        self.n_input = Entry(self.window, width=5)
        self.n_input.grid(column=1, row=6)
        self.n_input.insert(0, self.acad.solidity[1])
        Button(self.window, text="Файл", command=self.select_file).grid(column=0, row=7)
        Button(self.window, text="Цвет", command=self.set_color).grid(column=1, row=7)
        Button(self.window, text="ОК", command=self.submit).grid(column=0, row=8)
        Button(self.window, text="Cancel", command=self.quit).grid(column=1, row=8)
        self.set_up = True
        return self.window

    def check_setup(func):
        def wrapper(self, *args, **kwargs):
            if not self.set_up:
                print('Error: Resources in WindowGUI interface is not set up!')
                self.window.title('Ошибка')
                Label(self.window, text="Ошибка! Настройка окна не произведена. Используйте метод setup для настройки",
                      font=("Arial Bold", 12)).grid(column=0, row=0)
                return
            return func(self, *args, **kwargs)
        return wrapper

    @check_setup
    def get_point_coordinates(self):
        self.window.iconify()
        point = self.acad.set_point_coordinates()
        self.x_enter.delete(0, last=END)
        self.x_enter.insert(0, round(point[0], 2))
        self.y_enter.delete(0, last=END)
        self.y_enter.insert(0, round(point[1], 2))
        self.window.deiconify()

    @check_setup
    def select_file(self):
        filetypes = (
            ('JSON files', '*.json'),
            ('All files', '*.*')
        )
        filename = filedialog.askopenfilename(title='Выберите файл с данными', initialdir='/', filetypes=filetypes)
        self.acad.filepath = filename

    @check_setup
    def set_color(self):
        self.window.iconify()
        self.acad.set_color()
        self.window.deiconify()

    @check_setup
    def submit(self):
        try:
            x_point = float(self.x_enter.get())
            y_point = float(self.y_enter.get())
            solidity = [float(self.m_input.get()), float(self.n_input.get())]
        except ValueError:
            messagebox.showerror("Некорректное значение", "Вводимые значения должны быть числами (целыми либо с "
                                                          "плавающей точкой)!")
            return
        else:
            self.acad.point[0] = x_point
            self.acad.point[1] = y_point
            self.acad.solidity = solidity
            self.quit()

    def quit(self):
        self.window.destroy()


def main():
    acad = AutoCAD()
    gui = WindowGUI(acad)
    gui.setup().mainloop()
    print(acad.point)
    print(acad.solidity)


if __name__ == '__main__':
    main()
