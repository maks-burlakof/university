from CandyHierarchy import *


def main():
    choice = input('Выберите способ взаимодействия:\n1 - Заполнить массив значений с клавиатуры\n'
                   '2 - Использовать тестовые\n- - Выход\n >> ')
    if choice.strip() == '1':
        print('Создание базового объекта "Сладость".')
        sweet = Sweet(input('Название: '), float_input('Вес: ', 0.0))
        print('Создание объекта "Леденцовая конфета".')
        candy1 = Candy(input('Название: '), float_input('Вес: ', 0.0), input('Вкус: '))
        print('Создание объекта "Шоколад".')
        chocolate1 = Chocolate(input('Название: '), float_input('Вес: ', 0.0), input('Тип (горький/молочный): '),
                               float_input('Какао, %: ', 0.0, 100.0))
        print('Создание объекта "Леденец на палочке".')
        candy2 = CandyOnStick(input('Название: '), float_input('Вес: ', 0.0), input('Вкус: '), input('Форма: '))
        print('Создание объекта "Леденец в обертке".')
        candy4 = CandyInWrapper(input('Название: '), float_input('Вес: ', 0.0), input('Вкус: '), input('Тип обертки: '))
        gift = Gift(input('Имя получателя подарка: ')).add_sweets(sweet, chocolate1, candy1, candy2, candy4)
    elif choice.strip() == '2':
        sweet = Sweet('Халва узбекская молочная', 1000.0)
        chocolate1 = Chocolate('Коммунарка', 20.0, 'молочный', 75.0)
        chocolate2 = Chocolate('Столичный', 200.0, 'горький', 90.0)
        candy1 = Candy('Взлетная', 9.0, 'лимон')
        candy2 = CandyOnStick('Chupa Chups', 12.0, 'фруктовый', 'круглый')
        candy3 = CandyOnStick('Chupa Chups', 15.0, 'клубника', 'продолговатый')
        candy4 = CandyInWrapper('Барбарис', 10.0, 'барбарис, фруктовый', 'бумажная')
        gift = Gift("Максим Б.").add_sweets(sweet, chocolate1, chocolate2, candy1, candy2, candy3, candy4)
    else:
        print('Значение не выбрано. Завершение программы.')
        return

    print(f'Состав подарка:\n{gift}')
    print(f'Вес подарка: {gift.weight} г.')


def float_input(prompt: str, min_v: float, max_v: float = None) -> float:
    is_correct = False
    while not is_correct:
        try:
            value = float(input(prompt))
            condition = (min_v <= value) if not max_v else (min_v <= value <= max_v)
            assert condition
        except ValueError:
            print('Некорректное значение! Ожидается дробное или целое число, повторите попытку.')
        except AssertionError:
            print(f"Введенное значение должно удовлетворять интервалу [{min_v}, {(max_v if max_v else '..')}]")
        else:
            is_correct = True
    return value


if __name__ == '__main__':
    main()
