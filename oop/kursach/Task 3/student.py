class Student:
    def __new__(cls, name, group_number, grades):
        if not isinstance(name, str) or not isinstance(group_number, str):
            print('Traceback: Student object creation error: The values of name, group_number must be a string.')
            return None
        if not isinstance(grades, list) or len(grades) != 5:
            print('Traceback: Student object creation error: The value of grades must be a list of 5 elements.')
            return None
        for grade in grades:
            if not isinstance(grade, int):
                print('Traceback: Student object creation error: The grades list must contain integer values')
                return None
        return super(Student, cls).__new__(cls)

    def __init__(self, name: str, group_number: str, grades: list):
        self.name = name
        self.group_number = group_number
        self.grades = grades

    def __str__(self):
        return '{}, {}. Успеваемость: {}, {}, {}, {}, {}'.format(self.name, self.group_number, *self.grades)
