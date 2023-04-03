import re

class BookCard:
    def __new__(cls, *args, **kwargs):
        print(f'Новая запись успешно создана!')
        return super(BookCard, cls).__new__(cls)

    def __init__(self, author: str, title: str, publisher: str, pub_year: int, udc: str, circulation: int):
        self._author = author
        self._title = title
        self._publisher = publisher
        if 1800 <= pub_year <= 2023:
            self._pub_year = pub_year
        else:
            print(f'Ошибка! Некорректное значение поля "Год издания": {pub_year}. Ожидается в интервале [1800; 2023].')
            self._pub_year = None
        self._udc = udc
        if circulation > 0:
            self._circulation = circulation
        else:
            print(f'Ошибка! Некорректное значение поля "Тираж": {circulation}.')
            self._circulation = None
        self._rating = None

    def get_pub_year(self) -> int:
        return self._pub_year

    def set_rating(self, value: float):
        if 0 <= value <= 7:
            self._rating = value
        else:
            print(f'Ошибка! Некорректное значение рейтинга: {value}')

    def __del__(self):
        print(f'Запись книги "{self._title}" удалена')

    def __str__(self):
        return '{} ({}) - {}, {}г., {}.\nТираж: {}. Рейтинг: {}.'.\
            format(self._title, self._author, self._publisher, self._pub_year, re.sub(r"[^\w\s]", " ", self._udc),
                   self._circulation, self._rating)

    @staticmethod
    def sort_by_year(books: list):
        return sorted(books, key=lambda book: book.get_pub_year())


def int_input(prompt: str, min_v: int, max_v: int = None) -> int:
    is_correct = False
    while not is_correct:
        try:
            value = int(input(prompt))
            condition = (min_v <= value) if not max_v else (min_v <= value <= max_v)
            assert condition
        except ValueError:
            print('Некорректное значение! Ожидается целое число, повторите попытку.')
        except AssertionError:
            print(f"Введенное значение должно удовлетворять интервалу [{min_v}, {(max_v if max_v else '..')}]")
        else:
            is_correct = True
    return value


def main():
    choice = input('Выберите способ взаимодействия:\n1 - Заполнить массив значений с клавиатуры\n'
                   '2 - Использовать тестовые\n >> ')
    if choice.strip() == '1':
        books = []
        for i in range(1, 3):
            print('\nЗаполнение данных книги #{}'.format(i))
            books.append(BookCard(input('Автор: '), input('Заглавие: '), input('Издательство: '),
                                    int_input('Год издания: ', 1800, 2023), input('УДК: '), int_input('Тираж: ', 0)))
            books[-1].set_rating(int_input('Рейтинг: ', 0, 7))
        print('Вывод данных книг:')
        print("", *books, "", sep='\n\n')
        print('Отсортированные (по году издания) данные книг:')
        print("", *BookCard.sort_by_year(books), "", sep='\n\n')
    elif choice.strip() == '2':
        book1 = BookCard('Булгаков М.А.', 'Мастер и Маргарита', 'АСТ', 2001, '821.161.1-31', 13000)
        book1.set_rating(5.83)
        book2 = BookCard('Уальд О.', 'Портрет Дориана Грея', 'Питер', 2010, '821.111-31', 25000)
        book2.set_rating(5.95)
        print("", book1, book2, "", sep='\n\n')

        book3 = BookCard('Оруэлл Дж.', '1984', 'Эксмо', 2017, '821.121-31', 10000)
        book3.set_rating(5.70)
        book4 = BookCard('Дойл А.К.', 'Приключения Шерлока Холмса', 'ACT', 2015, '821.151-31', 5000)
        book4.set_rating(6.15)
        book5 = BookCard('Мартин Дж.Р.', 'Игра престолов', 'ACT', 2016, '821.181-31', 15000)
        book5.set_rating(6.82)
        book6 = BookCard('Толкин Д.Р.Р.', 'Властелин колец', 'Азбука', 2019, '821.111-31', 50000)
        book6.set_rating(6.62)
        sorted_books = BookCard.sort_by_year([book3, book4, book5, book6])
        print("", *sorted_books, "", sep='\n\n')
    else:
        print('Значение не выбрано. Завершение программы.')


if __name__ == "__main__":
    main()
