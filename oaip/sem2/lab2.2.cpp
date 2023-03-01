#include <iostream>
#include <conio.h>
using namespace std;

int* recurs(int*, int&, int&, int&);
int* non_recurs(int&, int&, int&);

int main() {
    setlocale(LC_ALL, "Russian");
    cout << "Задача 'Камушки'.\nПо окружности в направлении движения часовой стрелки расположены от 1 до n камней.\n"
        "При перемещении по камням с номерами 1, 2, ... каждый k-ый камень (k>1) удаляется. Этот процесс продолжается\n"
        "до тех пор, пока камней не станет меньше k. Определить номера и количество оставшихся камней.\n";
    int n, k, kol;
    while (1) {
        cout << "\nEnter the number of stones:\nLetter for random selection\n0 - EXIT\n >>> ";
        cin >> n;
        if (!cin) {
            cin.clear();
            while (cin.get() != '\n');
            srand(time(0));
            n = rand() % 30 + 10;    // 10..40
            cout << "Number of stones: " << n << "\n";
        }
        if (n == 0) break;
        if (n < 1) {
            cout << "Incorrect input!\n";
            continue;
        }
        cout << "Enter the k value:\n >>> ";
        while (!(cin >> k) || k < 1) {
            cout << "Incorrect input!\n >>> ";
            cin.clear();
            while (cin.get() != '\n');
        }
        cout << "\n 1 - Use a recursive function\n - - Use a regular function\n\n";
        switch (_getch()) {
        case '1': {
            cout << "A recursive function is used.\nThe numbers of the remaining stones: ";
            int* first_arr = new int[n];
            for (int i = 1; i <= n; i++) first_arr[i - 1] = i; //формируем массив
            kol = n;
            int poradok = 0;
            int* arr = recurs(first_arr, k, kol, poradok);
            for (int i = 0; i < kol; i++) cout << arr[i] << " ";
            cout << "\nThere are " << kol << " stones left\n";
            delete[] arr;
            break;
        }
        default: {
            cout << "The usual function is used.\nThe numbers of the remaining stones: ";
            int* arr = non_recurs(n, k, kol);
            for (int i = 0; i < kol; i++) cout << arr[i] << " ";
            cout << "\nThere are " << kol << " stones left\n";
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