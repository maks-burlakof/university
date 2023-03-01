#define _USE_MATH_DEFINES
#include <iostream>
#include <cmath>
using namespace std;
int main()
{
    //setlocale(LC_ALL, "Russian");
    double x, y, z, u;
    cout << "Enter x, y, z values: ";
    while (!(cin >> x >> y >> z)) {
        cout << "Incorrect input! Try again: ";
        cin.clear();
        while (cin.get() != '\n');
    }
    u = pow((8 + pow(fabs(x-y), 2) + 1), 1./3.) / (x*x + y*y + 2) - exp(fabs(x-y)) * pow((pow(tan(z), 2) + 1), x);
    cout << "Result: " << u;
    return 0;
}