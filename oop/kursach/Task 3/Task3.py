from student import Student
from db import Database, LocalMemory
from gui import GUI


def main():
    gui = GUI()
    gui.main_window().mainloop()


if __name__ == '__main__':
    main()
