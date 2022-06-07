#include <iostream>
#include <stdio.h>
#include <conio.h> 
using namespace std;

struct Stack {
	int info;
	Stack *next;
};

Stack *add (Stack*, int);
void view (Stack*);
void del(Stack**);
void task(Stack*&);
int input();

int main() {
	Stack *begin = NULL;
	int choice, n, a, b, in, stack_code;
	while (true) {
		cout << "--------- MENU ---------\n";
		cout << "1 - Create\n2 - Add\n3 - View\n"
			"4 - Individual task\n5 - Delete\n0 - EXIT\n";
		cout << "-------------------------\n >>> ";
		choice = input();
		system("cls");
		switch (choice) {
		case 1:
		case 2:
			if (begin && choice == 1) {
				cout << "The stack is not empty!\nClear memory!\n";
				break;
			}
			cout << "1 - Random\n2 - Test values\n3 - Keyboard\n >>> ";
			do {
				stack_code = input();
				cout << endl;
			} while (stack_code < 1 || stack_code > 3);
			if (stack_code == 2) { //test
				int arr[10] = { 4, 8, 1, -10, 2, 12, 5, 7, 0, 10 };
				for (int i = 0; i < 10; i++) begin = add(begin, arr[i]);
				cout << "Success!\n";
				break;
			}
			cout << " >>> Amount of elements = ";
			n = input();
			if (stack_code == 3) { //keyboard
				for (int i = 1; i <= n; i++) {
					cout << "\nEnter value # " << i << ": ";
					begin = add(begin, input());
				}
			}
			else { //random
				cout << "\n >>> [a, b] = ";
				a = input();
				cout << " ";
				b = input();
				srand(time(0));
				for (int i = 0; i < n; i++) {
					in = rand() % (b + 1 - a) + a;
					begin = add(begin, in);
				}
			}
			cout << "\nSuccess!\n";
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
			cout << "TASK: Remove elements with even numbers from the created list.\n";
			cout << "--- STACK BEFORE ---\n";
			view(begin);
			task(begin);
			cout << "--- STACK AFTER ---\n";
			view(begin);
			cout << "Success!\n";
			break;
		case 5:
			del(&begin);
			cout << "Stack deleted!\n";
			break;
		case 0:
			if (begin)
				del(&begin);
			return 0;
		}
	}
}

Stack *add(Stack *p, int element) {
	Stack *t = new Stack;
	t->info = element;
	t->next = p;
	return t;
}

void view(Stack *p) {
	Stack *t = p;
	while (t) {
		cout << t->info << endl;
		t = t->next;
	}
}

void del(Stack **p) {
	Stack *t;
	while (*p) {
		t = *p;
		*p = (*p)->next;
		delete t;
	}
}

void task(Stack *&p) {
	p = add(p, 1);
	Stack *t = p;
	Stack *t1 = p;
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
	return atoi(s);
}