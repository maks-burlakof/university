class Student:
    def __new__(cls, name, group_number, grades):
        if not name or not isinstance(name, str):
            raise ValueError('Фамилия и инициалы не могут быть пустой строкой.')
        if not group_number or not isinstance(group_number, str):
            raise ValueError('Номер группы не может быть пустой строкой.')
        if not isinstance(grades, list) or len(grades) != 5:
            raise ValueError('Traceback: Student object creation error: The value of grades must be a list of 5 elements.')
        for grade in grades:
            try:
                grade = int(grade)
                assert 1 <= grade <= 10
            except (ValueError, AssertionError):
                raise ValueError('Оценки должны быть целыми числами в диапазоне от 1 до 10')
        return super(Student, cls).__new__(cls)

    def __init__(self, name: str, group_number: str, grades: list):
        self.name = name
        self.group_number = group_number
        self.grades = [int(grade) for grade in grades]

    def __str__(self):
        return '{}, {}. Успеваемость: {}, {}, {}, {}, {}'.format(self.name, self.group_number, *self.grades)
