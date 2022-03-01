#include <iostream> // Индив на листе
#include <conio.h>
using namespace std;

int* recurs(int *arr, int &k, int &kol, int &poradok) {
    if (kol < k) return arr;
    for (int i = 0; i < kol; i++) {
        poradok++;
        //cout << "poradok = " << poradok << "\n";//
        if (poradok == k) { //удалить элемент, сдвинуть массив, kol--, poradok = 0.
            //cout << "Удален элемент " << arr[i] << "\n";//
            for (int j = i; j < kol - 1; j++) arr[j] = arr[j + 1];
            kol--;
            i--;
            poradok = 0;
            //cout << "Остались элементы:\n";//
            //for (int i = 0; i < kol; i++) cout << arr[i] << " ";//
            //cout << "\n";//
        }
    }
    return recurs(arr, k, kol, poradok);
}

int* non_recurs(int& n, int& k, int& kol) {
    kol = n;
    int poradok = 0;
    int *arr = new int[n];
    for (int i = 1; i <= n; i++) arr[i-1] = i;
    while (kol >= k) {
        //cout << "Новый проход цикла\nОстались элементы:\n";//
        //for (int i = 0; i < kol; i++) cout << arr[i] << " ";//
        //cout << "\n";//
        for (int i = 0; i < kol; i++) {
            poradok++;
            //cout << "poradok = " << poradok << "\n";//
            if (poradok == k) {
                //cout << "Удален элемент " << arr[i] << "\n";//
                for (int j = i; j < kol-1; j++) arr[j] = arr[j+1];
                kol--;
                i--;
                poradok = 0;
                //cout << "Остались элементы:\n";//
                //for (int i = 0; i < kol; i++) cout << arr[i] << " ";//
                //cout << "\n";//
            }
        }
    }
    //cout << "Выход из while";//
    //cout << "Ответ: kol = " << kol << ", остались элементы:\n";//
    //for (int i = 0; i < kol; i++) cout << arr[i] << " ";//
    //cout << "\n";//
    return arr;
}

int main() {
    setlocale(LC_ALL, "Russian");
    srand(time(0));
    int n, k, kol;
    cout << "Количество камней:\nИли буква для случайного выбора\n";
    cin >> n;
    if (!cin) {
        cin.clear();
        while (cin.get() != '\n');
        n = rand() % 30 + 10;    // 10..40
        cout << n << "\n";
    }
    cout << "Введите k: ";
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
        for (int i = 1; i <= n; i++) first_arr[i-1] = i; //формируем массив
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
    return 0;
}