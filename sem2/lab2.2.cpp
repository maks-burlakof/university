#include <iostream>
#include <conio.h>
using namespace std;

int* recurs(int*, int&, int&, int&);
int* non_recurs(int&, int&, int&);

int main() {
    setlocale(LC_ALL, "Russian");
    srand(time(0));
    int n, k, kol;
    while (1) {
        cout << "\nКоличество камней:\nБуква для случайного выбора\n0 - Выход\n>>> ";
        cin >> n;
        if (n == 0) break;
        if (!cin) {
            cin.clear();
            while (cin.get() != '\n');
            n = rand() % 30 + 10;    // 10..40
            cout << n << "\n";
        }
        cout << "Введите k: \n>>> ";
        while (!(cin >> k)) {
            cout << "Введите целое число: \n";
            cin.clear();
            while (cin.get() != '\n');
        }

        cout << "\n1 - Использовать рекурсивную функцию\n2 - Использовать обычную функцию\n\n";
        switch (_getch()) {
        case '1': {
            cout << "Использована рекурсивная функция.\nОтвет: ";
            int* first_arr = new int[n];
            for (int i = 1; i <= n; i++) first_arr[i - 1] = i; //формируем массив
            kol = n;
            int poradok = 0;
            int* arr = recurs(first_arr, k, kol, poradok);
            for (int i = 0; i < kol; i++) cout << arr[i] << " ";
            cout << "\nОсталось камней: " << kol << endl;
            delete[] arr;
            break;
        }
        default: {
            cout << "Использована обычная функция.\nОтвет: ";
            int* arr = non_recurs(n, k, kol);
            for (int i = 0; i < kol; i++) cout << arr[i] << " ";
            cout << "\nОсталось камней: " << kol << endl;
            delete[] arr;
            break;
        }
        }
    }
    return 0;
}

int* recurs(int* arr, int& k, int& kol, int& poradok) {
    if (kol < k) return arr;
    for (int i = 0; i < kol; i++) {
        poradok++;
        if (poradok == k) {
            for (int j = i; j < kol - 1; j++) arr[j] = arr[j + 1];
            kol--;
            i--;
            poradok = 0;
        }
    }
    return recurs(arr, k, kol, poradok);
}

int* non_recurs(int& n, int& k, int& kol) {
    kol = n;
    int poradok = 0;
    int* arr = new int[n];
    for (int i = 1; i <= n; i++) arr[i - 1] = i;
    while (kol >= k) {
        for (int i = 0; i < kol; i++) {
            poradok++;
            if (poradok == k) {
                for (int j = i; j < kol - 1; j++) arr[j] = arr[j + 1];
                kol--;
                i--;
                poradok = 0;
            }
        }
    }
    return arr;
}