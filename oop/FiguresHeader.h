#include <iostream>
#include <cmath>

using namespace std;

class Square {
public:
    double len;

    Square() {
        len = 1;
    }

    Square(double l) {
        len = l;
    }

    double diagonal() {
        return sqrt(2) * len;
    }

    double perimeter() {
        return 4 * len;
    }

    double square() {
        return len * len;
    }

    void print() {
        cout << "Фигура: Квадрат\n"
                "Длина стороны: " << len << "\n"
                "Диагональ: " << diagonal() << "\n"
                "Периметр: " << perimeter() << "\n"
                "Площадь: " << square() << "\n";
    }

    ~Square() {
        cout << "Деструктор вызван для объекта квадрата с len = " << len << "\n";
    }
};

class Pyramid : public Square {
public:
    double apothem;  // может ее в private?

    Pyramid(): Square() {
        apothem = 1;
    }

    Pyramid(double l, double a): Square(l) {
        apothem = a;
    }

    double square() {
        return (0.5 * len * apothem) + (len * len);
    }

    double height() {
        return sqrt(pow(apothem, 2) - pow((diagonal() / 2.), 2));
    }

    double volume() {
        return 1/3. * height() * len * len;
    }

    void print() {
        cout << "Фигура: Правильная четырехугольная пирамида\n"
                "Длина стороны основания: " << len << "\n"
                "Длина высоты: " << height() << "\n"
                "Площадь:" << square() << "\n"
                "Объём: " << volume() << "\n";
    }

    ~Pyramid() {
        cout << "Деструктор вызван для объекта пирамиды с apothem = " << apothem << "\n";
    }
};