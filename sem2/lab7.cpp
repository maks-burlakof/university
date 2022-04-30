#include <iostream>
#include <cmath>
using namespace std;

double fun(double x);
double derivative(double x);
double solve(double x0, double eps);
void poisk(double a, double b, double eps);
double input();

int main() {
	double a, b, eps;
	cout << "Function: x^2 - 10sin(x)^2 + 2\n";
	cout << "Enter a value:\n >>> ";
	a = input();
	cout << "Enter b value:\n >>> ";
	b = input();
	cout << "Enter eps value:\n >>> ";
	eps = input();
	poisk(a, b, eps);
	return 0;
}

double fun(double x) {
	return x * x - 10 * sin(x) * sin(x) + 2;
}

double derivative(double x) {
	return 2 * x - 10 * sin(2 * x);
}

double solve(double x0, double eps) {
	double x1 = x0 - fun(x0) / derivative(x0);
	while (fabs(x1 - x0) > eps) {
		x0 = x1;
		x1 = x0 - fun(x0) / derivative(x0);
	}
	return x1;
}

void poisk(double a, double b, double eps) {
	for (double x = a; x <= b; x += eps)
		cout << "x = " << x << "\ty = " << fun(x) << endl;
	cout << "~~~~~~~~~~~~~~~~~~~~\n";
	for (double x = a; x <= b; x += eps) {
		if (fun(x) * fun(x + eps) < 0) {
			cout << "Root = " << solve(x, eps) << endl;
		}
	}
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