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




//int main() {
	//    setlocale(LC_ALL, "Russian");
	//    char name[81], date[81];
	//    int amount, price, n = 0;
	//    cout << "n = ? ";
	//    cin >> n;
	//    Tovar* products = new Tovar[n];
	//    for (int i = 0; i < n; i++) {
	//        cout << "Enter product name, amount of products, unit price, date of delivery:\n";
	//        cin >> name >> amount >> price >> date;
	//        //Tovar obj(name, amount, price, date);
	//        products[i] = Tovar(name, amount, price, date);
	//    }
	//
	//    while (true) {
	//        cout << "\n~~~~~~~~~~ MENU ~~~~~~~~~~\n "
	//            "1 - Add object\n "
	//            "2 - View object data\n "
	//            "3 - Total cost of products\n "
	//            "4 - Delete object\n "
	//            "0 - EXIT\n";
	//        switch (_getch()) {
	//        case 1:
	//            system("cls");
	//            cout << "Enter product name, amount of products, unit price, date of delivery:\n";
	//            cin >> name >> amount >> price >> date;
	//            // Tovar obj(name, amount, price, date);
	//            Tovar* products = new[1];
	//            n++;
	//            products[n] = Tovar(name, amount, price, date);
	//            break;
	//        case 2:
	//            system("cls");
	//            cout << "Enter product name: ";
	//            cin >> name;
	//            for (int i = 0; i < n; i++) {
	//                if (strcmp(products[i].name, name) == 0) {
	//                    products[i].printInfo();
	//                    break;
	//                }
	//            }
	//            break;
	//        case 3:
	//            system("cls");
	//            cout << "Enter product name: ";
	//            cin >> name;
	//            for (int i = 0; i < n; i++) {
	//                if (products[i].name == name) cout << "Total cost of products: " << products[i].getTotalPrice();
	//            }
	//            break;
	//        case 4:
	//            system("cls");
	//            break;
	//        case 0:
	//            system("cls");
	//            // вызвать деструктор
	//            return 0;
	//        default:
	//            system("cls");
	//            break;
	//        }
	//    }
	//    return 0;
	//}
