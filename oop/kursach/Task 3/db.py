import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def create_conn(self):
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)

    def close_conn(self):
        self.conn.close()

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

    def create_table(self):
        self.execute_command('''CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
                                group_number TEXT NOT NULL,
                                grade1 INTEGER,
                                grade2 INTEGER,
                                grade3 INTEGER,
                                grade4 INTEGER,
                                grade5 INTEGER);''', ())

    def add_student(self, student):
        self.execute_command("INSERT INTO students (name, group_number, grade1, grade2, grade3, grade4, grade5) VALUES (?, ?, ?, ?, ?, ?, ?, ?);",
                             (student.last_name, student.initials, student.group_number, student.grades[0],
                              student.grades[1], student.grades[2], student.grades[3], student.grades[4]))

    def get_students(self):
        students = self.execute_command_select("SELECT * FROM students;")
        return students
