#include <iostream> // К элементам массива по индексу обращаться через указатель
#include <conio.h>
using namespace std;

//void summa(int*, int, int*);
//void proizv(int*, int, int&);
void poisk(int*, int, int*, int&);

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
    int* arr = new int[n];
    cout << "Выберите:\n\t" << "1 - заполнить массив вручную\n\t2 - заполнить массив случайными числами\n";
    switch (_getch()) {
    case '1':
        cout << "Заполните массив из " << n << " элементов:\n\t";
        for (int i = 0; i < n; i++) cin >> *(arr + i);
        break;
    default:
        cout << "Введите диапазон значений случайных чисел [a, b]: ";
        int a, b;
        cin >> a >> b;
        srand(time(0));
        for (int i = 0; i < n; i++) {
            *(arr + i) = rand() % (b + 1 - a) + a;
            cout << *(arr + i) << "  ";
        }
        break;
    }
    int sum = -1, proiz = 0;
    poisk(arr, n, &sum, proiz);
    if (sum < 0) cout << "\nПоложительных элементов нет"; else cout << "\nСумма положительных элементов: " << sum;
    if (proiz == 0) cout << "\nОтрицательных элементов нет"; else cout << "\nПроизведение отрицательных элементов: " << proiz << endl;
    delete[] arr;
    return 0;
}

//void summa(int *arr, int n, int *sum) {
//    for (int i = 0; i < n; i++) if (*(arr + i) > 0) *sum += *(arr + i);
//}
//
//void proizv(int *arr, int n, int &proiz) {
//    for (int i = 0; i < n; i++) if (*(arr + i) < 0) proiz *= *(arr + i);
//}

void poisk(int* arr, int n, int* sum, int& proiz) {
    for (int i = 0; i < n; i++) {
        if (*(arr + i) > 0) if (*sum < 0) *sum += *(arr + i) + 1; else *sum += *(arr + i);
        if (*(arr + i) < 0) if (proiz == 0) {
            proiz = 1;
            proiz *= *(arr + i);
        }
        else proiz *= *(arr + i);
    }
}