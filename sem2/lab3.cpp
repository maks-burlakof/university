// Обязательно добавить проверки

#include <iostream>
#include <stdio.h>
using namespace std;

struct Stack {
	int info;
	Stack *next, *begin;
};

Stack *add (Stack*, int);
void view (Stack*);
void del(Stack**);
void task(Stack*&);

int main() {
	Stack *begin = NULL;
	int choice, n, a, b, in;
	while (true) {
		cout << "--------- MENU ---------\n";
		cout << "1 - Create\n2 - Add\n3 - View\n"
			"4 - Individual task\n5 - Delete\n0 - EXIT\n";
		cout << "-------------------------\n >>> ";
		cin >> choice;
		system("cls");
		switch (choice) {
		case 1:
		case 2:
			if (begin != NULL && choice == 1) {
				cout << "The stack is not empty!\nClear memory!\n";
				break;
			}
			cout << " >>> Amount of elements = ";
			cin >> n;
			cout << " >>> [a, b] = ";
			cin >> a >> b;
			srand(time(0));
			for (int i = 0; i < n; i++) {
				in = rand() % (b + 1 - a) + a;
				begin = add(begin, in); // вершину стека ставим на новый элемент
			}
			cout << "Success!\n";
			break;
		case 3:
			if (!begin) {
				cout << "Stack is empty!\n";
				break;
			}
			cout << "--- STACK ---\n";
			view(begin);
			break;
		case 4:
			if (!begin) {
				cout << "Stack is empty!\n";
				break;
			}
			task(begin);
			cout << "Success!\n";
			break;
		case 5:
			del(&begin);
			cout << "Stack deleted!\n";
			break;
		case 0:
			if (begin != NULL)
				del(&begin);
			return 0;
		}
	}
}

Stack *add(Stack *p, int element) {
	Stack *t = new Stack;
	t->info = element;
	t->next = p; // записываем адрес предыдущего элемента
	return t;
}

void view(Stack *p) {
	Stack *t = p;
	while (t) {
		cout << t->info << endl;
		t = t->next; // Переставляем текущий указатель t на следующий за ним элемент
	}
}

void del(Stack **p) {
	Stack *t;
	while (*p) {
		t = *p; // Устанавливаем текущий указатель на вершину
		*p = (*p)->next; // Вершину переставляем на следующий элемент
		delete t; // Освобождаем память бывшей вершины
	}
}

void task(Stack *&p) {
	p = add(p, 1);
	Stack* t = p;
	Stack* t1 = p;
	t = t->next;
	while (t) {
		if (t->info % 2 != 0) {
			t1 = t;
			t = t->next;
		}
		else {
			t1->next = t->next;
			delete t;
			t = t1->next;
		}
	}
	t = p;
	p = p->next;
	delete t;
}

//Stack* task(Stack* p) {
//	Stack* t = p;
//	Stack* t1 = p;
//	while (t) {
//		if (t->info % 2 != 0) {
//			t1 = t;
//			t = t->next;
//		}
//		else {
//			if (t == p) {
//				p = p->next;
//				delete t;
//				return p;
//			}
//			else {
//				t1->next = t->next;
//				delete t;
//				t = t1->next;
//			}
//		}
//	}
//}