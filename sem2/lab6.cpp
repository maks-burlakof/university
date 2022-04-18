#include <iostream> // Удалить элемент по ключу
#include <conio.h>  // Создать сбалансированное дерево
using namespace std; // Объеденить два case по добавлению, в case 1 создание дерева сразу добавить добавление case 2

struct Tree {
    int info;
    Tree *left, *right;
};

Tree *List(int);
Tree *create(Tree *);
void Add_List(Tree*, int);
void view(Tree*, int);
Tree *del(Tree*);
int input();

int main() {
    Tree *root = NULL;
    int choice, in, n, a, b, in_code;
    while (true) {
        cout << "--------- MENU ---------\n";
        cout << "1 - Create\n2 - Add\n3 - View\n"
            "4 - Individual task\n5 - Delete\n0 - EXIT\n";
        cout << "-------------------------\n >>> ";
        choice = input();
        system("cls");
        switch (choice) {
        case 1:
            if (root) {
                cout << "Error!\nClear memory!\n"; // можем ли вообще удалить корень?
                break;
            }
            cout << " >>> Input Root : ";
            in = input();
            root = List(in);
            cout << "\nSuccess!\n";
            break;
        case 2:
            cout << "1 - Random\n2 - Keyboard\n3 - Test values\n >>> ";
            do {
                in_code = input();
                cout << endl;
            } while (in_code < 1 || in_code > 3);
            if (in_code == 3) {
                int arr[10] = { 4, 8, 1, -10, 2, 12, 5, 7, 0, 10 };
                for (int i = 0; i < 5; i++) {
                    if (!root) root = List(arr[i]);
                    else Add_List(root, arr[i]);
                }
                cout << "Success!\n";
                break;
            }
            cout << " >>> Amount of elements = ";
            n = input();
            if (in_code == 2) {
                for (int i = 0; i < n; i++) {
                    cout << " Input info #" << i << ": ";
                    in = input();
                    // здесь поиск по ключу (и добавить i-- и continue)
                    if (!root) root = List(in);
                    else Add_List(root, in);
                }
            }
            else {
                cout << "\n >>> [a, b] = ";
                a = input();
                cout << " ";
                b = input();
                srand(time(0));
                for (int i = 0; i < n; i++) {
                    in = rand() % (b + 1 - a) + a;
                    // здесь поиск по ключу (и добавить i-- и continue)
                    if (!root) root = List(in);
                    else Add_List(root, in);
                }
            }
            cout << "\nSuccess!\n";
            view(root, 0);
            break;
        case 3:
            if (!root) {
                cout << "Tree not created!\nCreate it by pressing 1\n";
                break;
            }
            view(root, 0); // Второй параметр определяет уровень (level), на котором находится узел.
            break;
        case 4:
            if (!root) {
                cout << "Tree not created!\nCreate it by pressing 1\n";
                break;
            }
            //task();
            cout << "Success!\n";
            break;
        case 5:
            root = del(root);
            cout << "Tree removed!\n";
            break;
        case 0:
            if (root)
                root = del(root);
            return 0;
        }
    }
}

Tree *List(int in) {
    Tree* t = new Tree;
    t->info = in;
    t->left = t->right = NULL;
    return t;
}

void Add_List(Tree *root, int in) {
    Tree *prev = NULL, *t = root;
    bool is_find = 0;
    while (t && !is_find) {
        prev = t;
        if (in == t->info) {
            is_find = 1;
            cout << "Element " << in << " already exists\n";
        }
        else {
            if (in < t->info) t = t->left;
            else t = t->right;
        }
    }
    if (!is_find) {
        t = List(in);
        if (in < prev->info) prev->left = t;
        else prev->right = t;
    }
}

void view(Tree *t, int level) {
    if (t) {
        view(t->right, level + 1);
        for (int i = 0; i < level; i++)
            cout << "    ";
        cout << t->info << endl;
        view(t->left, level + 1);
    }
}

// Функция поиска по ключу
// Функция удаления элемента по ключу

Tree *del(Tree* t) {
    if (t) {
        del(t->left);
        del(t->right);
        delete t;
    }
    return NULL;
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
            cout << "--del\n";
        }
        if (!(s[i] >= '0' && s[i] <= '9' || s[i] == '-')) continue;
        cout << s[i];
        i++;
    }
    s[i] = '\0';
    cout << endl;
    return atoi(s);
}