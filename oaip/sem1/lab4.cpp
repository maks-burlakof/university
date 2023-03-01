#include <iostream>
#include <math.h>
#include <iomanip>
using namespace std;
typedef double (*uf)(double, double, int&);
void Out_Rez(double, double, double, double, uf);
double y(double, double, int&);
double s(double, double, int&);
int main() {
	setlocale(LC_ALL, "Russian");
	double a, b, h, eps;
	cout << "Enter a, b, h, eps: ";
	while (!(cin >> a >> b >> h >> eps))
	{
		cout << "Неверный ввод! Повторите попытку: \n";
		cin.clear();
		while (cin.get() != '\n');
	}
	cout << setw(8) << "x" << setw(15) << "y(x)" << setw(10) << "k" << endl;
	Out_Rez(a, b, h, eps, y);
	cout << endl;
	cout << setw(8) << "x" << setw(15) << "s(x)" << setw(10) << "k" << endl;
	Out_Rez(a, b, h, eps, s);
	return 0;
}
void Out_Rez(double a, double b, double h, double eps, uf fun) {
	int k = 0;
	double sum;
	for (double x = a; x < b + h / 2; x += h) {
		sum = fun(x, eps, k);
		cout << setw(8) << x << setw(15) << sum << setw(10) << k << endl;
	}
}
double y(double x, double eps, int& k) {
	return x*atan(x) - log(pow((x*x + 1), 0.5));
}
double s(double x, double eps, int& k) {
	double a, c, sum;
	sum = a = c = x;
	k = 1;
	while (fabs(c) > eps) {
		c = pow(x, 2*k) / (2*k * (2*k - 1));
		a *= -c;
		sum += a;
		k++;
	}
	return sum;
}