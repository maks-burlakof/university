#include <iostream>
#include <conio.h>
using namespace std;

void poisk(int*, int, int*, int&);
int input();

int main() {
    setlocale(LC_ALL, "Russian");
    cout << "Задание: В одномерном массиве, состоящем из n элементов целого типа, найти:\n"
        "Сумму положительных(У) и произведение отрицательных элементов(С).\n"
        "Искомые параметры передать в функцию main по ссылке &(C) или по указателю *(У)\n";
    int n;
    do {
        cout << "\nEnter the size of the array:\n >>> ";
        n = input();
    } while (n < 1);
    int* arr = new int[n];
    cout << "\nChoose:\n\t" << "1 - fill array manually\n\t- - fill array with random numbers\n >>> ";
    switch (input()) {
    case 1:
        cout << "\nFill in the array of " << n << " elements:\n >>> ";
        for (int i = 0; i < n; i++) {
            *(arr + i) = input();
            cout << " ";
        }
        break;
    default:
        cout << "\nEnter a range of random number values [a, b]:\n >>> ";
        int a, b;
        a = input();
        cout << "\n >>> ";
        b = input();
        cout << "\n";
        srand(time(0));
        for (int i = 0; i < n; i++) {
            *(arr + i) = rand() % (b + 1 - a) + a;
            cout << *(arr + i) << "  ";
        }
        break;
    }
    int sum = -1, proiz = 0;
    poisk(arr, n, &sum, proiz);
    if (sum < 0) cout << "\nThere are no positive elements"; else cout << "\nSum of positive elements: " << sum;
    if (proiz == 0) cout << "\nThere are no negative elements"; else cout << "\nMultiplication of negative elements: " << proiz << endl;
    delete[] arr;
    return 0;
}

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

int input() {
    char s[20];
    int i = 0;
    while (true) {
        s[i] = _getch();
        if (s[i] == 13 || s[i] == ' ') { // enter
            if (i == 0) continue;
            else break;
        }
        if (s[i] == 8) { // backspace
            if (i == 0) continue;
            for (int j = 0; j <= i; j++) {
                s[j] = '\0';
            }
            i = 0;
            cout << "--del\n >>> ";
        }
        if (!(s[i] >= '0' && s[i] <= '9' || s[i] == '-')) continue;
        cout << s[i];
        i++;
    }
    s[i] = '\0';
    return atoi(s);
}