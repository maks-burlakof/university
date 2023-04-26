from os import path
import sqlite3

from student import Student


class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def execute_command(self, command: str, params: tuple):
        if self.conn is not None:
            self.conn.execute(command, params)
            self.conn.commit()
        else:
            raise ConnectionError("You need to create connection to database!")

    def execute_command_select(self, command: str):
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(command)
            return cur.fetchall()
        else:
            raise ConnectionError("You need to create connection to database!")

    def start(self):
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.execute_command("CREATE TABLE IF NOT EXISTS students (name TEXT NOT NULL, group_number TEXT NOT NULL, "
                             "grade1 INTEGER, grade2 INTEGER, grade3 INTEGER, grade4 INTEGER, grade5 INTEGER);", ())

    def stop(self):
        self.conn.close()

    def add_student(self, name: str, group: str, grades: list):
        self.execute_command("INSERT INTO students (name, group_number, grade1, grade2, grade3, grade4, grade5) "
                             "VALUES (?, ?, ?, ?, ?, ?, ?);",
                             (name, group, grades[0], grades[1], grades[2], grades[3], grades[4]))

    def get_data(self):
        students = self.execute_command_select("SELECT * FROM students;")
        return [list(elem) for elem in students]

    def clear_data(self):
        """
        Clear all records in `students` table, without table deleting.
        """
        self.execute_command("DELETE FROM students;", ())


class LocalMemory:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.db = Database(db_name)
        self.db.start()
        self.data = self.db.get_data()

    def __del__(self):
        self.db.stop()

    @property
    def is_changed(self):
        return not self.data == self.db.get_data()

    def add_student(self, student: Student):
        self.data.append([student.name, student.group_number, student.grades[0], student.grades[1],
                          student.grades[2], student.grades[3], student.grades[4]])

    def delete_students(self, selection):
        for record in sorted(selection, reverse=True):
            del self.data[record]

    def open(self, filepath):
        """
        Return is_error, message
        """
        filename_full = path.basename(filepath)
        filename, extension = path.splitext(filepath)
        if not extension:
            return True, "Файл должен содержать расширение"
        if extension not in ['.db', '.sqlite3']:
            return True, "Расширение файла должно быть .db или .sqlite3"
        try:
            db_new = Database(filepath)
            db_new.start()
            data_new = db_new.get_data()
        except Exception:
            return True, "Ошибка при открытии базы данных."
        else:
            self.db.stop()
            self.db = db_new
            self.db_name = filename_full
            self.data = data_new
            return False, f"Открыта база данных: {filename_full}"

    def save(self, filename):
        """
        Return is_error, message
        """
        if not self.is_changed:
            return False, "Данные не изменены, сохранять не требуется."
        self.db.clear_data()
        for student in self.data:
            self.db.add_student(student[0], student[1], [int(student[2]), int(student[3]), int(student[4]),
                                                         int(student[5]), int(student[6])])
        return False, "База данных сохранена в файл: {}".format(filename)

    def search(self, phrase, only_name=False):
        phrase = phrase.strip().lower()
        results = []
        for person in self.data:
            if only_name:
                if phrase in person[0].lower().strip():
                    results.append(person)
            else:
                if phrase in person[0].lower().strip() or phrase in person[1].lower().strip():
                    results.append(person)
        return results

    def search_without_scholarship(self):
        results = []
        for person in self.data:
            if min([int(person[2]), int(person[3]), int(person[4]), int(person[5]), int(person[6])]) <= 4:
                results.append(person)
        return results
