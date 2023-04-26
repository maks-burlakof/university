from student import Student
from db import Database, LocalMemory
from gui import GUI


def main():
    db = Database('students.db')
    db.start()

    memory = LocalMemory(db)
    gui = GUI(memory)
    gui.main_window().mainloop()

    gui.db.stop()


if __name__ == '__main__':
    main()
