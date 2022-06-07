#include <iostream>
using namespace std;

struct Stack {
	char s;
	Stack* next;
};

int getPrioritet(char);
void push(Stack*&, char);
void out(Stack*&, char&);
double Result(char*);
bool expressionCheck(char *);
double input();

int main() {
	char formula[81], final[81], ss_buff;
	int final_len = 0;
	Stack *begin = NULL;
	do {
		cout << " Input formula: ";
		cin >> formula;
	} while(!expressionCheck(formula));
	for (int i = 0; formula[i] != '\0'; i++) {
		char ss = formula[i];
		if (ss >= 'a' && ss <= 'z') final[final_len++] = ss;
		if (ss == '(') push(begin, ss);
		if (ss == ')') {
			while (begin->s != '(') {
				out(begin, ss_buff);
				final[final_len++] = ss_buff;
			}
			out(begin, ss_buff);
		}
		if (ss == '-' || ss == '+' || ss == '*' || ss == '/') {
			while (begin != NULL && getPrioritet(begin->s) >= getPrioritet(ss)) {
				out(begin, ss_buff);
				final[final_len++] = ss_buff;
			}
			push(begin, ss);
		}
	}
	while (begin != NULL) {
		out(begin, ss_buff);
		final[final_len++] = ss_buff;
	}
	final[final_len] = '\0';
	cout << endl << "Polish notation of the formula: " << final << endl;
	cout << "Result: " << Result(final);
	return 0;
}

int getPrioritet(char s) {
	if (s == '*' || s == '/') return 2;
	if (s == '+' || s == '-') return 1;
	if (s == '(') return 0;
	return NULL;
}

void push(Stack*& top, char s) {
	Stack* t = new Stack;
	t->s = s;
	if (t == NULL) {
		top = t;
	}
	else {
		t->next = top;
		top = t;
	}
}

void out(Stack*& top, char& buff) {
	Stack* q = top;
	buff = q->s;
	if (q == top)
	{
		top = q->next;
		free(q);
	}
	else
		free(q);
	q = q->next;
}

double Result(char* str) {
	Stack* begin = NULL;
	char ss, ss1, ss2, ssR = 'z' + 1;
	double op1, op2, res, mas[50];
	cout << "Input data: ";
	for (int i = 0; str[i] != '\0'; i++) {
		ss = str[i];
		if (ss >= 'a' && ss <= 'z') {
			cout << ss << " = ";
			mas[int(ss - 'a')] = input();
		}
	}
	for (int i = 0; str[i] != '\0'; i++) {
		ss = str[i];
		if (!(ss == '+' || ss == '-' || ss == '*' || ss == '/' || ss == '^'))
			push(begin, ss);
		else {
			out(begin, ss2);
			out(begin, ss1);
			op2 = mas[int(ss2 - 'a')];
			op1 = mas[int(ss1 - 'a')];
			switch (ss) {
			case '+': res = op1 + op2;  break;
			case '-': res = op1 - op2;  break;
			case '*': res = op1 * op2;  break;
			case '/': res = op1 / op2;  break;
			}
			mas[int(ssR - 'a')] = res;
			push(begin, ssR);
			ssR++;
		}
	}
	return res;
}

bool expressionCheck(char* In) {
	int errors = 0, bracket = 0;
	if (In[0] == '+' || In[0] == '-' || In[0] == '*' || In[0] == '/' || (In[0] == ')')) {
		cout << "You can't put signs and closing bracket at the beginning\n";
		errors++;
	}
	if (In[1] == '\0' || In[2] == '\0') {
		cout << "Expression is not complete\n";
		errors++;
	}
	for (int i = 0; In[i] != '\0'; i++) {
		if (!(In[i] >= 'a' && In[i] <= 'z') && In[i] != '+' && In[i] != '-' && In[i] != '*' && In[i] != '/' && In[i] != '(' && In[i] != ')') {
			cout << "Unresolved character: " << In[i] << endl;
			errors++;
		}
		if (In[i] == '(') {
			if (In[i + 1] == '+' || In[i + 1] == '-' || In[i + 1] == '*' || In[i + 1] == '/' || In[i + 1] == ')') {
				cout << "You can't put signs and closing bracket after opening bracket\n";
				errors++;
			}
			if (In[i + 1] == NULL) {
				cout << "Expression is not complete\n";
				errors++;
			}
			if (In[i + 2] == ')') {
				cout << "Expression in brackets is not complete\n";
				errors++;
			}
			bracket++;
		}
		if (In[i] == ')') {
			if ((In[i + 1] >= 'a' && In[i + 1] <= 'z') || In[i + 1] == '(') {
				cout << "You must put a sign after the closing bracket\n";
				errors++;
			}
			bracket--;
		}
		if (In[i] >= 'a' && In[i] <= 'z') {
			if (In[i + 1] >= 'a' && In[i + 1] <= 'z') {
				cout << "Enter two letters in a row is unavailable\n";
				errors++;
			}
			if (In[i + 1] == '(') {
				cout << "You can't put open bracket after letters\n";
				errors++;
			}
		}
		if (In[i] == '+' || In[i] == '-' || In[i] == '*' || In[i] == '/') {
			if (In[i + 1] == '+' || In[i + 1] == '-' || In[i + 1] == '*' || In[i + 1] == '/') {
				cout << "Enter two signs in a row is unavailable\n";
				errors++;
			}
			if (In[i + 1] == ')') {
				cout << "You can't put closing bracket after signs\n";
				errors++;
			}
			if (In[i + 1] == NULL) {
				cout << "Expression is not completed\n";
				errors++;
			}
		}
	}
	if (bracket != 0) {
		cout << "Check brackets and try one more time.. \n";
		errors++;
	}
	if (!errors) return 1;
	else return 0;
}

double input() {
	double in;
	while (!(cin >> in) or cin.get() != '\n') {
		cout << "Invalid input! Try again:\n >>> ";
		cin.clear();
		while (cin.get() != '\n');
	}
	return in;
}