#include <iostream>
#include <cmath>
#include <conio.h>
using namespace std;
int main()
{
    setlocale(LC_ALL, "Russian");
    cout << "Enter a, b, z values: ";
    double a, b, z, x, func, y;  
    while (!(cin >> a >> b >> z)) {
        cout << "Incorrect input! Try again: ";
        cin.clear();
        while (cin.get() != '\n');
    }
    if (z < 1) x = 2 + z;
    else x = pow(sin(z), 2);
    cout << "Select the function:\n\t1) 2x\n\t2) x*x\n\t3) x/3\n";
    switch (_getch()) {
        case '1': func = 2*x; break;
        case '2': func = x*x; break;
        case '3': func = x/3; break;
        default: 
            cout << "Error!\nYou can choose only 1, 2, 3\n";
            return 0;
    }
    y = ((2*a*func) + (b*cos(sqrt(fabs(x))))) / (x*x + 5);
    printf("Вычисления проводились с a = %8.6lf, b = %8.6lf, z = %8.6lf.\nВ ходе выполнения программы "
        "x = %8.6lf.\nЗначение выбранной функции: %8.6lf.\nРезультат: %8.6lf", a, b, z, x, func, y);
}