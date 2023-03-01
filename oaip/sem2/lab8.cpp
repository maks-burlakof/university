#include <iostream>
#include <conio.h>
using namespace std;

double func(double);
double metod(double (*f)(double), double, double, int);
double input();

int main() {
	double a, b, eps, I1, I2, pogr;
	int n;
	cout << "Function: x^2 - 10(sin x)^2\na = 0, b = 3, Integral value = -6.699\n";
	do {
		//system("cls");
		cout << "\n >>> Input a, b: ";
		a = input();
		b = input();
		cout << "\nChoose work method:\n 1 - Calculation on the number of fragmentation n\n"
			" - - Eps precision calculation\n >>> ";
		if (input() == 1) {
			cout << "\n >>> Input n: ";
			n = input();
			I1 = metod(func, a, b, n);
		}
		else {
			cout << "\n >>> Input eps: ";
			eps = input();
			n = 2;
			I1 = metod(func, a, b, n);
			do {
				n *= 2;
				I2 = metod(func, a, b, n);
				pogr = fabs(I2 - I1);
				I1 = I2;
			} while (pogr > eps);
			cout << "\n Required number n = " << n;
		}
		cout << "\n Integral value = " << I1 << endl;
		cout << "\n Choose an action:\n 1 - Repeat\n - - EXIT\n >>> ";
	} while (input() == 1);
	return 0;
}

double func(double x) {
	return x * x - 10 * sin(x) * sin(x);
}

double metod(double (*f)(double x), double a, double b, int n) {
	double s = 0, h, x = a;
	h = (b - a) / n;
	for (int i = 1; i <= n; i++) {
		s += (f(x) + f(x + h)) / 2;
		x += h;
	}
	return h * s;
}

double input() {
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
		if (!(s[i] >= '0' && s[i] <= '9' || s[i] == '-' || s[i] == '.')) continue;
		cout << s[i];
		i++;
	}
	s[i] = '\0';
	cout << " ";
	return atof(s);
}