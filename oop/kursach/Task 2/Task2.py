from CandyHierarchy import *


def main():
    sweet = Sweet('Халва узбекская молочная', 1000)
    chocolate1 = Chocolate('Коммунарка', 20, 'молочный', 75)
    chocolate2 = Chocolate('Столичный', 200, 'горький', 90)
    candy1 = Candy('Взлетная', 9, 'лимон')
    candy2 = CandyOnStick('Chupa Chups', 12, 'фруктовый', 'круглый')
    candy3 = CandyOnStick('Chupa Chups', 15, 'клубника', 'продолговатый')
    candy4 = CandyInWrapper('Барбарис', 10, 'барбарис, фруктовый', 'бумажная')

    gift = Gift("Максим Б.").add_sweets(sweet, chocolate1, chocolate2, candy1, candy2, candy3, candy4)

    print(f'Состав подарка:\n{gift}')
    print(f'Вес подарка: {gift.weight} г.')


if __name__ == '__main__':
    main()
