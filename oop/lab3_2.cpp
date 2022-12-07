#include <iostream>
#include "FiguresHeader.h"

double input();
void fillArray(Square*, int, int);
Square* addElement(Square*, int);
double find_min_square(Square*, int);
void fillArray(Pyramid*, int, int);
Pyramid* addElement(Pyramid*, int);
int find_pyramids_num(Pyramid*, double, int);

int main() {
    setlocale(LC_ALL, "Russian");
    int n, m;
    cout << "Введите количество квадратов N:\n";
    cin >> n;
    Square* squares = new Square[n];
    fillArray(squares, 0, n);

    cout << "Введите количество пирамид M:\n";
    cin >> m;
    Pyramid* pyramids = new Pyramid[m];
    fillArray(pyramids, 0, n);

    int in;
    while (true) {
        cout << "\n~~~~~~~~~~ МЕНЮ ~~~~~~~~~~\n "
                "1 - Добавить объект типа Квадрат\n "
                "2 - Добавить объект типа Пирамида\n "
                "3 - Просмотр текущего состояния объектов типа Квадрат\n "
                "4 - Просмотр текущего состояния объектов типа Пирамида\n "
                "5 - Найти наименьшую площадь квадрата\n "
                "6 - Найти число пирамид с высотой больше a\n "
                "0 - ВЫХОД\n";
        cin >> in;
        switch(in) {
            case 0:
                return 0;
            case 1:
                squares = addElement(squares, n);
                n++;
                break;
            case 2:
                pyramids = addElement(pyramids, m);
                m++;
                break;
            case 3:
                for (int i = 0; i < n; i++) {
                    squares[i].print();
                    cout << "\n";
                }
                break;
            case 4:
                for (int i = 0; i < m; i++) {
                    pyramids[i].print();
                    cout << "\n";
                }
                break;
            case 5:
                cout << "Минимальная найденная площадь квадрата: " << find_min_square(squares, n) << endl;
                break;
            case 6:
                cout << "Введите число а для поиска пирамид с высотой, большей а (через Enter): \n";
                double a = input();
                cout << "Число пирамид с высотой большей a: " << find_pyramids_num(pyramids, a, n) << endl;
                break;
        }
    }
    return 0;
}

void fillArray(Square* massiv, int start, int end) {
    cout << "Введите длину стороны для " << end-start << " квадратов(-a):\n";
    for (int i = start; i < end; i++) {
        cout << "#" << i + 1 << ".\n";
        massiv[i] = Square(input());
    }
}

Square* addElement(Square* massiv, int number) {
    int numTemp = number + 1;
    Square* temp = new Square[numTemp];
    for (int i = 0; i < number; i++) temp[i] = massiv[i];
    fillArray(temp, number, numTemp);
    delete[] massiv;
    return temp;
}

double find_min_square(Square* massiv, int n) {
    double min_square = massiv[0].square();
    for (int i = 0; i < n; i++)
        if (massiv[i].square() < min_square)
            min_square = massiv[i].square();
    return min_square;
}

void fillArray(Pyramid* massiv, int start, int end) {
    cout << "Введите длину основания и длину апофемы " << end-start << " пирамид (через Enter):\n";
    for (int i = start; i < end; i++) {
        cout << "#" << i + 1 << ".\n";
        massiv[i] = Pyramid(input(), input());
    }
}

Pyramid* addElement(Pyramid* massiv, int number) {
    int numTemp = number + 1;
    Pyramid* temp = new Pyramid[numTemp];
    for (int i = 0; i < number; i++) temp[i] = massiv[i];
    fillArray(temp, number, numTemp);
    delete[] massiv;
    return temp;
}

int find_pyramids_num(Pyramid* massiv, double a, int n) {
    int counter = 0;
    for (int i = 0; i < n; i++)
        if (massiv[i].height() > a)
            counter ++;
    return counter;
}

double input() {
    double in;
    while (!(cin >> in)) {
        cout << "Введенное значение должно быть числом! Повторите попытку.\n >>> ";
        cin.clear();
        while (cin.get() != '\n');
    }
    return in;
}