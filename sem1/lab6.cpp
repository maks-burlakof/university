#include <iostream>
#include <conio.h>
using namespace std;
int main()
{
    setlocale(LC_ALL, "Russian");
    int n, m, i, j;
    do {
        cout << "Введите n, m: ";
        cin >> n >> m;
    } while (n > 50 || n < 1 || m > 50 || m < 2);
    int **arr = new int*[n];
    cout << "Выберите:\n\t" << "1 - заполнить массив вручную\n\t2 - заполнить массив случайными числами\n";
    switch (_getch()) {
    case '1':
        cout << "Заполните двумерный массив\n";
        for (i = 0; i < n; i++) {
            arr[i] = new int[m];
            for (j = 0; j < m; j++) cin >> arr[i][j];
        }
        break;
    default:
        cout << "Введите диапазон значений случайных чисел [a, b]: ";
        int a, b;
        cin >> a >> b;
        srand(time(0));
        for (int i = 0; i < n; i++) {
            arr[i] = new int[m];
            for (j = 0; j < m; j++) {
                arr[i][j] = rand() % (b + 1 - a) + a;
                cout << arr[i][j] << "\t";
            }
            cout << "\n";
        }
        break;
    }
    cout << endl;
    int *b = new int[n];
    for (i = 0; i < n; i++) {
        b[i] = 1;
        for (j = 0; j < m - 1; j++) {
            if (arr[i][j] <= arr[i][j + 1]) {
                b[i] = 0;
                break;
            }
        }
        cout << b[i] << " ";
    }
    for (i = 0; i < n; ++i) delete[]arr[i];
    delete[]arr;
    delete[]b;
    return 0;
}