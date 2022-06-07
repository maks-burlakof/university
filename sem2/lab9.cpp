#include <iostream>
#include <string>
using namespace std;

struct Stack {
	char s;
	Stack *next;
};

int getPrioritet(char);


bool isNumberNumeric()
{
	if (cin.get() == '\n')
		return true;
	else
	{
		cin.clear();
		cin.ignore(numeric_limits<streamsize>::max(), '\n');
		return false;
	}
}

double inputNumber()
{
	double number;
	while (true)
	{
		cin >> number;
		if (isNumberNumeric())
		{
			return number;
		}
		else
		{
			cout << "Incorrect input!\nTry again: ";
		}
	}
}

void pushInStack(Stack *&top, char s) {
	Stack *t = new Stack;
	t->s = s;
	if (t == NULL) {
		top = t;
	}
	else {
		t->next = top;
		top = t;
	}
}

void out(Stack *&top, char& buff) {
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

int getPrioritet(char s) {
	if (s == '*' || s == '/') return 2;
	if (s == '+' || s == '-') return 1;
	if (s == '(') return 0;
	return NULL;
}


double countingInPolishNotation(Stack*& begin, string final, double a, double b, double c, double d, double e)
{
	char ss, comp1, comp2;
	double op1, op2, rez = 0;

	double mas[201]; // Массив для вычисления 

	// Работаем с символами 
	mas[int('a')] = a; // в ячейку (a --> код ASCII) заполняем введенное значение a 
	mas[int('b')] = b;
	mas[int('c')] = c;
	mas[int('d')] = d;
	mas[int('e')] = e;


	char chr = 'z' + 1; // chr --> ячейка с элементом после табличного z 

	for (int i = 0; i < final.length(); i++) // Цикл для перебора всех символов в финальной строке (преобразованной) 
	{
		ss = final[i]; // По очереди символ из строки final заносим в ss для обработки 

		if (ss >= 'a' && ss <= 'z')  // Заносим в стек если НЕ оператор
			pushInStack(begin, ss);
		else
		{
			out(begin, comp1);  // Выносим 2 переменные из стека
			out(begin, comp2);

			op1 = mas[int(comp1)];
			op2 = mas[int(comp2)];

			switch (ss)
			{
			case '*':
				rez = op2 * op1;
				break;
			case '/':
				rez = op2 / op1;
				break;
			case '+':
				rez = op2 + op1;
				break;
			case '-':
				rez = op2 - op1;
				break;
			case '^':
				rez = pow(op2, op1);
			}

			mas[int(chr)] = rez; // Ячейка с символом следующим после z в таблице ASCII --> результат вычисления
			pushInStack(begin, chr);
			chr++;
		}
	}

	return rez;
}


int main() {
	string formulaString, final;

	char ss_buff;
	Stack* begin = NULL;


	cout << "Enter formula: ";
	cin >> formulaString;
	//formulaString = "a/b-((c+d)*e)";
	int length = formulaString.length();

	for (int i = 0; i < length; i++)
	{
		char ss = formulaString[i];

		if (ss >= 'a' && ss <= 'z') //выгружаем в final 
			final += ss;

		if (ss == '(')
			pushInStack(begin, ss);

		if (ss == ')') //Выталкиваем все до открывающейся скобки
		{
			while (begin->s != '(')
			{
				out(begin, ss_buff);
				final += ss_buff;
			}
			out(begin, ss_buff); // Удаляем )
		}



		if (ss == '-' || ss == '+' || ss == '*' || ss == '/')
		{
			while (begin != NULL && getPrioritet(begin->s) >= getPrioritet(ss))
			{
				out(begin, ss_buff);
				final += ss_buff;
			}
			pushInStack(begin, ss);
		}
	}

	while (begin != NULL)
	{
		out(begin, ss_buff);
		final += ss_buff;
	}
	// Окончание строки
	cout << endl << "Polish notation of the formula: " << final << endl;


	double a, b, c, d, e;
	cout << "Enter a: ";
	do {
		a = inputNumber();
		if (a > 100 || a < -100)
			cout << "You can use only -100 - 100. Try again: ";
	} while (a > 100 || a < -100);
	cout << "Enter b: ";
	do {
		b = inputNumber();
		if (b > 100 || b < -100)
			cout << "You can use only -100 - 100. Try again: ";
	} while (b > 100 || b < -100);
	cout << "Enter c: ";
	do {
		c = inputNumber();
		if (c > 100 || c < -100)
			cout << "You can use only -100 - 100. Try again: ";
	} while (c > 100 || c < -100);
	cout << "Enter d: ";
	do {
		d = inputNumber();
		if (d > 100 || d < -100)
			cout << "You can use only -100 - 100. Try again: ";
	} while (d > 100 || d < -100);
	cout << "Enter e: ";
	do {
		e = inputNumber();
		if (e > 100 || e < -100)
			cout << "You can use only -100 - 100. Try again: ";
	} while (e > 100 || e < -100);

	cout << "Result: " << countingInPolishNotation(begin, final, a, b, c, d, e) << endl;
	return 0;
}