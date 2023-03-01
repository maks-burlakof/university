#pragma once
#include <iostream>

using namespace std;

class Tovar {
private:
	int amount;
	double price;
	char date[81];
public:
	char name[81];
	Tovar() {
		strcpy_s(name, "");
		amount = 0;
		price = 0;
		strcpy_s(date, "");
	}
	Tovar(char* str, int n, double cost, char* d) {
		strcpy_s(name, str);
		amount = n;
		price = cost;
		strcpy_s(date, d);
	}
	void printInfo() {
		cout << " -> Product name: " << name << endl <<
			" -> Amount: " << amount << endl <<
			" -> Unit price: " << price << endl <<
			" -> Date of delivery: " << date << endl;
	}
	double getTotalPrice();
	~Tovar() {
		cout << "Object " << name << " deleted";
	}
};


double Tovar::getTotalPrice() {
	return amount * price;
}