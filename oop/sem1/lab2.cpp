#include <iostream>
#include <conio.h>
#include "TovarHeader.h"
using namespace std;

int main() {
    setlocale(LC_ALL, "Russian");
    char name[81], date[81];
    int amount, n = 0;
	double price;
	cout << " >>> Enter amount of products: n = ";
    cin >> n;
    Tovar* products = new Tovar[n];
    for (int i = 0; i < n; i++) {
        cout << "#" << i+1 << ". Enter product name, amount of products, unit price, date of delivery:\n >>> ";
        cin >> name >> amount >> price >> date;
        products[i] = Tovar(name, amount, price, date);
    }
    cout << "\tDisplay product information\n >>> Enter product name: ";
    cin >> name;
    for (int i = 0; i < n; i++) {
        if (strcmp(products[i].name, name) == 0) {
            products[i].printInfo();
            break;
        }
		cout << "No products found with this name\n";
    }
	cout << "\tCalculate total cost\n >>> Enter product name: ";
	cin >> name;
	for (int i = 0; i < n; i++) {
		if (strcmp(products[i].name, name) == 0) {
			cout << "Total price is " << products[i].getTotalPrice() << "$\n";
			break;
		}
		cout << "No products found with this name\n";
	}
    delete[] products;
    return 0;
}
