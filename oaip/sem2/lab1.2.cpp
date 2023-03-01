#include <iostream>
using namespace std;

struct Database {
	int Free;
	char Time[20];
	char Destination[20];
};

void In(Database*, int);
void Out(Database*, int);
void Poisk(Database*, int, int&);
int input();

int main() {
	setlocale(LC_ALL, "Russian");
	cout << "На ж/д вокзале хранится информация о свободных местах в поездах. Информация в списке: время отправления,\n"
		"пункт назначения, число свободных мест. Вывести информацию о поездах до Бреста, в порядке убывания количества\n"
		"свободных мест и их количество.\n\n";
	int i, n, kol = 0;
	do {
		cout << " Number of trains = ";
		n = input();
	} while (n < 1);
	Database *Trains = new Database[n];
	In(Trains, n);
	cout << "\n\n Train information:";
	for (i = 0; i < n; i++) Out(Trains, i);
	cout << "\n\n Destination: 'Brest':";
	Poisk(Trains, n, kol);
	cout << "\n\n Found trains: " << kol << endl;
	delete[] Trains;
	return 0;
}

void In(Database *Trains, int n) {
	for (int i = 0; i < n; i++) {
		cout << "#" << i+1 << "\nDestination: ";
		cin >> (Trains + i)->Destination;
		cout << "Departure time: ";
		cin >> (Trains + i)->Time;
		cout << "Number of available places: ";
		(Trains + i)->Free = input();
	}	
}

void Out(Database *Train, int i) {
	cout << "\nDestination: " << (Train + i)->Destination << "| Departure time: " <<
		(Train + i)->Time << "| Number of available places: " << (Train + i)->Free;
}

void Poisk(Database *Trains, int n, int& kol) {
	for (int i = 0; i < n - 1; i++) { // sort all trains
		for (int j = i + 1; j < n; j++) {
			if ((Trains + i)->Free < (Trains + j)->Free) {
				Database TempTrain = Trains[i];
				Trains[i] = Trains[j];
				Trains[j] = TempTrain;
			}
		}
	}
	for (int i = 0; i < n; i++) {
		if (!strcmp((Trains + i)->Destination, "Brest")) {
			kol++;
			Out(Trains, i);
		}
	}
}

int input() {
	int in;
	while (!(cin >> in) or cin.get() != '\n') {
		cout << "Invalid input! Try again:\n >>> ";
		cin.clear();
		while (cin.get() != '\n');
	}
	return in;
}