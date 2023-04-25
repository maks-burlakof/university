from student import Student
from db import Database
from gui import GUI


def main():
    st = Student('Бурлаков М. В.', '122402', [1, 2, 3, 4, 5])
    print(st)

    db = Database('students.db')
    db.start()

    gui = GUI(db)
    gui.main_window().mainloop()

    db.stop()


if __name__ == '__main__':
    main()
