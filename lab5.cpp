#include <iostream>
#include <conio.h>
#include <ctime>
using namespace std;
int main()
{
    setlocale(LC_ALL, "Russian");
    int n;
    cout << "Введите размер массива: ";
    while (!(cin >> n) || (n > 50 || n < 1))
    {
        cout << "Неверный ввод! Повторите попытку: ";
        cin.clear();
        while (cin.get() != '\n');
    }
    int *arr = new int[n];
    cout << "Выберите:\n\t" << "1 - заполнить массив вручную\n\t2 - заполнить массив случайными числами\n";
    int inp;
    do inp = _getch();
        while (inp != 49 && inp != 50);
    switch (inp) {
    case '1':
        cout << "Заполните массив из " << n << " элементов:\n\t";
        for (int i = 0; i < n; i++) cin >> arr[i];
        break;
    default:
        cout << "Введите диапазон значений случайных чисел [a, b]: ";
        int a, b;
        cin >> a >> b;
        srand(time(0));
        for (int i = 0; i < n; i++) {
            arr[i] = rand() % (b + 1 - a) + a;
            cout << arr[i] << "  ";
        }
        break; 
    }
    int i1 = -1, i2 = -1;
    for (int i = 0; i < n; i++) {
        if (arr[i] == 0) {
            i1 = i;
            break;
        }
    }
    if (i1 < 0) {
        cout << "\nВ массиве нет нулей\n";
        delete[] arr; return 0;
    }
    for (int i = n - 1; i > i1; i--) {
        if (arr[i] == 0) {
            i2 = i;
            break;
        }
    }
    if (i2 < 0) {
        cout << "\nВ массиве только один ноль\n";
        delete[] arr; return 0;
    }
    if (i2 - i1 == 1) {
        cout << "\nНули в массиве находятся рядом\n";
        delete[] arr; return 0;
    }
    int sum = 0;
    for (int i = i1 + 1; i < i2; i++) sum += arr[i];
    cout << "\nСумма = " << sum << endl;
    delete[] arr; return 0;
}