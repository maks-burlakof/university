#include <iostream>
#include <conio.h>  // balanced
using namespace std;

struct Tree {
    int info;
    Tree *left, *right;
};

Tree *list(int);
Tree *create(Tree*);
void add(Tree*, int);
void view(Tree*, int);
void task(Tree*, int &);
Tree *del_elem(Tree*, int);
Tree *del(Tree*);
Tree* uniq_check(Tree*, int);
int input();

int main() {
    Tree *root = NULL;
    int choice, in, n, a, b, in_code = 1, amount, key;
    while (true) {
        cout << "--------- MENU ---------\n";
        cout << "1 - Create\n2 - Add\n3 - View\n"
            "4 - Individual task\n5 - Delete element\n6 - Delete tree\n0 - EXIT\n";
        cout << "-------------------------\n >>> ";
        choice = input();
        system("cls");
        switch (choice) {
        case 1:
            if (root) {
                cout << "Error!\nClear memory by pressing 5\n";
                break;
            }
            cout << " >>> Input root: ";
            in = input();
            root = list(in);
            cout << "\nSuccess!\n";
            break;
        case 2:
            cout << "1 - Random\n2 - Keyboard\n3 - Test values\n >>> ";
            do {
                in_code = input();
                cout << endl;
            } while (in_code < 1 || in_code > 3);
            if (in_code == 3) { // test
                int arr[10] = { 12, 3, 0, -2, 5, 25, 17, 1, 30, 52};
                for (int i = 0; i < 10; i++) {
                    if (!root) root = list(arr[i]);
                    else add(root, arr[i]);
                }
                cout << "Success!\n";
                view(root, 0);
                break;
            }
            cout << " >>> Amount of elements = ";
            n = input();
            if (in_code == 2) { // keyboard
                for (int i = 1; i <= n; i++) {
                    cout << " Input info #" << i << ": ";
                    in = input();
                    if (uniq_check(root, in)) {
                        cout << "This element already exists!\n";
                        i--;
                    }
                    if (!root) root = list(in);
                    else add(root, in);
                }
            }
            else { // random
                cout << "\n >>> [a, b] = ";
                a = input();
                cout << " ";
                b = input();
                srand(time(0));
                for (int i = 0; i < n; i++) {
                    in = rand() % (b + 1 - a) + a;
                    if (uniq_check(root, in)) {
                        cout << "This element already exists!\n";
                        i--;
                    }
                    if (!root) root = list(in);
                    else add(root, in);
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
            view(root, 0);
            break;
        case 4:
            if (!root) {
                cout << "Tree not created!\nCreate it by pressing 1\n";
                break;
            }
            amount = 0;
            task(root, amount);
            cout << "Number of leaves in a tree: " << amount << ".\nSuccess!\n";
            view(root, 0);
            break;
        case 5:
            if (!root) {
                cout << "Tree not created!\nCreate it by pressing 1\n";
                break;
            }
            cout << "~ Find the numbers of leaves in a tree ~\n";
            cout << " >>> Enter key value: ";
            cin >> key;
            cout << "Before:\n";
            view(root, 0);
            root = del_elem(root, key);
            cout << "After:\n";
            view(root, 0);
            cout << "Success!\n";
            break;
        case 6:
            root = del(root);
            cout << "Tree removed!\n";
            break;
        case 0:
            if (root) root = del(root);
            return 0;
        }
    }
}

Tree *list(int in) {
    Tree* t = new Tree;
    t->info = in;
    t->left = t->right = NULL;
    return t;
}

void add(Tree *root, int in) {
    Tree *prev = NULL, *t = root;
    while (t) {
        prev = t;
        if (in < t->info) t = t->left;
        else t = t->right;
    }
    t = list(in);
    if (in < prev->info) prev->left = t;
    else prev->right = t;
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

void task(Tree *t, int &amount) {
    if (t) {
        task(t->left, amount);
        task(t->right, amount);
        if (t->right == 0 and t->left == 0) {
            amount++;
        }
    }
}

Tree *del_elem(Tree *root, int key)
{
    Tree *del = root, *del_prev = NULL, *repl, *repl_prev;
    while (del && del->info != key) {
        del_prev = del;
        if (del->info > key) del = del->left;
        else del = del->right;
    }
    if (!del) {
        cout << "Element not found!\n";
        return root;
    }
    if (del->right == NULL) repl = del->left;
    else {
        if (del->left == NULL) repl = del->right;
        else {
            // Ищем самый правый в левом поддереве
            repl = del->left;
            repl_prev = del;
            while (repl->right) {
                repl_prev = repl;
                repl = repl->right;
            }
            if (repl_prev == del) repl->right = del->right;
            else {
                repl->right = del->right;
                repl_prev->right = repl->left;
                repl->left = repl_prev;
            }
        }
    }
    if (del == root) root = repl;
    else {
        if (del->info < del_prev->info) del_prev->left = repl;
        else del_prev->right = repl;
    }
    delete del;
    return root;
}

Tree *del(Tree *t) {
    if (t) {
        del(t->left);
        del(t->right);
        delete t;
    }
    return NULL;
}

Tree *uniq_check(Tree *t, int key) {
    while (t && t->info != key) {
        if (t->info > key) t = t->left;
        else t = t->right;
    }
    return t;
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