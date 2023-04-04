from CandyHierarchy import *


def main():
    chocolate1 = Chocolate('Коммунарка', 20, 'молочный', 75)
    chocolate2 = Chocolate('Столичный', 200, 'горький', 90)
    candy1 = CandyOnStick('Chupa Chups', 12, 'фруктовый', 'круглый')
    candy2 = CandyOnStick('Chupa Chups', 15, 'клубника', 'продолговатый')
    candy3 = CandyInWrapper('Барбарис', 10, 'барбарис, фруктовый', 'бумажная')

    gift = Gift("Максим Б.").add_sweet(chocolate1).add_sweet(chocolate2).add_sweet(candy1).add_sweet(candy2).add_sweet(candy3)

    print('Вес подарка: ', gift.weight)
    print(f'Состав подарка:\n{gift}')


if __name__ == '__main__':
    main()
