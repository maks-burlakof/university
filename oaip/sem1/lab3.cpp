#include <iostream>
#include <cmath>
#include <iomanip>
using namespace std;
int main()
{
    setlocale(LC_ALL, "Russian");
    cout << "Enter a, b, h, n values: ";
    double a, b, h, n, s, y, r;
    while (!(cin >> a >> b >> h >> n)) {
        cout << "Неверный ввод! Повторите попытку: \n";
        cin.clear();
        while (cin.get() != '\n');
    }
    for (double x = a; x <= b; x += h) {
        r = -1;
        s = 0;
        for (int k = 1; k <= n; k++) {
            r = -r * x * x;
            s += r / (2 * k * (2 * k - 1));
        }
        y = x * atan(x) - log(pow((x * x + 1), 0.5));
        cout << left << "X = " << setw(10) << x << "Y(x) = " << setw(15) << y << "S(x) = " << setw(15) << s << "|Y(x) - S(x)| = " << abs(y - s) << endl;
    }
    return 0;
}