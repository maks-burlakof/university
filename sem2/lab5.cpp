#include <iostream>
#include <conio.h>
using namespace std;

struct list {
	int info;
	list *prev, *next;
};

void create(list**, list**, int);
void add(int, list**, list**, int);
void view(int, list*);
void del(list**);
void task(list*&, list *&);
int input();

int main() {
	list *begin = NULL, *end = NULL, *t;
	int choice, list_code, n, a, b, in;
	while (true) {
		cout << "--------- MENU ---------\n";
		cout << "1 - Create\n2 - Add\n3 - View\n"
			"4 - Individual task\n5 - Delete\n0 - EXIT\n";
		cout << "-------------------------\n >>> ";
		choice = input();
		system("cls");
		switch (choice) {
		case 1:
			if (begin) {
				cout << "Error!\nClear memory!\n";
				break;
			}
			cout << " >>> Begin info = ";
			in = input();
			create(&begin, &end, in);
			cout << "\nSuccess!\n";
			break;
		case 2:
			if (!begin) {
				cout << "List is empty!\nCreate a list by pressing 1\n";
				break;
			}
			cout << "1 - Random: Add to begin\n2 - Random: Add to end\n3 - Test values\n"
				"4 - Keyboard: Add to begin\n5 - Keyboard: Add to end\n >>> ";
			do {
				list_code = input();
				cout << endl;
			} while (list_code < 1 || list_code > 5);
			if (list_code == 3) {
				int arr[10] = {4, 8, 1, -10, 2, 12, 5, 7, 0, 10};
				for (int i = 0; i < 5; i++) add(1, &begin, &end, arr[i]);
				for (int i = 5; i < 10; i++) add(2, &begin, &end, arr[i]);
				cout << "Success!\n";
				break;
			}
			cout << " >>> Amount of elements = ";
			n = input();
			if (list_code == 4 || list_code == 5) {
				cout << "\nEnter values:\n";
				for (int i = 0; i < n; i++) {
					add(5-list_code, &begin, &end, input());
					cout << endl;
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
					add(list_code, &begin, &end, in);
				}
			}
			cout << "\nSuccess!\n";
			break;
		case 3:
			if (!begin) {
				cout << "List is empty!\nCreate a list by pressing 1\n";
				break;
			}
			cout << "1 - Show from begin\n2 - Show from end\n >>> ";
			do {
				list_code = input();
				cout << endl;
			} while (list_code != 1 && list_code != 2);
			if (list_code == 1) t = begin;
			else t = end;
			cout << "--- LIST ---\n";
			view(list_code, t);
			break;
		case 4:
			if (!begin) {
				cout << "List is empty!\nCreate a list by pressing 1\n";
				break;
			}
			cout << "TASK: Remove elements with even numbers from the created list.\n";
			cout << "--- LIST BEFORE ---\n";
			view(1, begin);
			task(begin, end);
			cout << "--- LIST AFTER ---\n";
			view(1, begin);
			cout << "Success!\n";
			break;
		case 5:
			del(&begin);
			cout << "List deleted!\n";
			break;
		case 0:
			if (begin)
				del(&begin);
			return 0;
		}
	}
    return 0;
}

void create(list **begin, list **end, int in) {
	list *t = new list;
	t->info = in;
	t->next = t->prev = NULL;
	*begin = *end = t;
}

void add(int list_code, list **begin, list **end, int in) {
	list *t = new list;
	t->info = in;
	if (list_code == 1) {
		t->prev = NULL;
		t->next = *begin;
		(*begin)->prev = t;
		*begin = t;
	}
	else {
		t->next = NULL;
		t->prev = *end;
		(*end)->next = t;
		*end = t;
	}
}

void view(int list_code, list *t) {
	while (t) {
		cout << t->info << endl;
		if (list_code == 1) t = t->next;
		else t = t->prev;
	}
}

void del(list **p) {
	list *t;
	while (*p) {
		t = *p;
		*p = (*p)->next;
		delete t;
	}
}

void task(list *&begin, list *&end) {
	list *t = begin, *t_del;
	while (t) {
		if (t->info % 2 == 0) {
			if (t == begin) {
				begin = begin->next;
				if (begin) begin->prev = NULL;
			}
			else {
				if (t == end) {
					end = end->prev;
					end->next = NULL;
				}
				else {
					(t->prev)->next = t->next;
					(t->next)->prev = t->prev;
				}
			}
			t_del = t;
			t = t->next;
			delete t_del;
		}
		else {
			t = t->next;
		}
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
			cout << "--del\n";
		}
		if (!(s[i] >= '0' && s[i] <= '9' || s[i] == '-')) continue;
		cout << s[i];
		i++;
	}
	s[i] = '\0';
	return atoi(s);
}