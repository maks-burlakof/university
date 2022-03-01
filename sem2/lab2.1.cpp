#include <iostream>
#include <conio.h>      // При вводе числа, которого нет в массиве, результат проги будет каким-то числом, но не 0
using namespace std;   //// - нужна проверка

int recurs(int &a, int &b, int elem, int arr[]) {
    int c = (a + b) / 2;
    if (arr[c] == elem || b - a == 1) return c + 1;
    if (arr[c] > elem) return recurs(a, c, elem, arr);
    else return recurs(c, b, elem, arr);
}

int non_recurs(int &a, int &b, int elem, int arr[]) {
    int c = 0;
    do {
        c = (a + b) / 2;
        if (arr[c] > elem) b = c;
        else a = c;
    } while (elem != arr[c] && b - a != 1);
    return c + 1;
}

int main() {
    setlocale(LC_ALL, "Russian");
    srand(time(0));
    int n, elem;
    cout << "Введите размер массива или букву для выбора случайно: ";
    cin >> n;
    if (!cin) {
        cin.clear();
        while (cin.get() != '\n');
        n = rand() % 18 + 2;    // от 2 до 20
        cout << n << "\n";
    }
    int* arr = new int[n];
    cout << "\n1 - Ввести значения с клавиатуры\n2 - Случайные значения\n\n";
    switch (_getch()) {
    case '1':
        cout << "Заполните массив из " << n << " элементов:\n";
        for (int i = 0; i < n; i++) cin >> arr[i]; ////
        break;
    default:
        arr[0] = rand() % 10 + 1;    // от 1 до 11
        cout << arr[0] << "  ";
        for (int i = 1; i < n; i++) {
            arr[i] = arr[i-1] + rand() % 5 + 1;
            cout << arr[i] << "  ";
        }
        break;
    }
    cout << "\n\nЧисло: ";
    cin >> elem; ////
    cout << "\n1 - Использовать рекурсивную функцию\n2 - Использовать обычную функцию\n\n";
    int a = 0, b = n - 1;
    switch (_getch()) {
    case '1': cout << "Использована рекурсивная функция. Номер элемента - " << recurs(a, b, elem, arr); break;
    default: cout << "Использована обычная функция. Номер элемента - " << non_recurs(a, b, elem, arr); break;
    }
    cout << endl;
    return 0;
}