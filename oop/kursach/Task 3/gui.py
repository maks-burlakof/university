import tkinter as tk

from db import Database
from student import Student


class GUI:
    def __init__(self, db: Database):
        self.db = db
        self.window = tk.Tk()
        self.window.title("Student Records")
        # self.window.iconbitmap('img/people.ico')

    def test_window(self):
        pass

    def main_window(self):
        self.window.geometry('1000x700')

        # Create labels and entry fields for student information
        label_name = tk.Label(self.window, text="Name:")
        entry_name = tk.Entry(self.window)
        label_group_number = tk.Label(self.window, text="Group Number:")
        entry_group_number = tk.Entry(self.window)
        label_grades = tk.Label(self.window, text="Grades (separated by commas):")
        entry_grades = tk.Entry(self.window)

        # Create buttons for adding and viewing students
        button_add_student = tk.Button(self.window, text="Add Student", command=self.add_student_window)
        button_view_students = tk.Button(self.window, text="View Students", command=self.view_students_window)

        # Place labels and entry fields in the window
        label_name.grid(row=0, column=0)
        entry_name.grid(row=0, column=1)
        label_group_number.grid(row=2, column=0)
        entry_group_number.grid(row=2, column=1)
        label_grades.grid(row=3, column=0)
        entry_grades.grid(row=3, column=1)
        button_add_student.grid(row=4, columnspan=2)

        return self.window

    def add_student_window(self):
        pass

    def view_students_window(self):
        pass
