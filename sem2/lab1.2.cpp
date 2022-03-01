#include <iostream>
using namespace std;

struct Database {
	int Free;
	char Time[20];
	char Destination[20];
} *Train;

void In(int n) {
	for (int i = 0; i < n; i++) {
		cout << "\nDestination: ";
		cin >> (Train + i)->Destination;
		cout << "Departure time: ";
		cin >> (Train + i)->Time;
		cout << "Number of available places: ";
		while (!(cin >> (Train + i)->Free)) {
			cout << "Incorrect int value. Try again: \n";
			cin.clear();
			while (cin.get() != '\n');
		}
	}
}

void Out(int i) {
	cout << "\n Destination: " << (Train + i)->Destination << "| Departure time: " << 
		(Train + i)->Time << "| Number of available places: " << (Train + i)->Free;
}

void Poisk(Database* Train, int n, int& kol) {
	for (int i = 0; i < n - 1; i++) // sort all trains
		for (int j = i + 1; j < n; j++)
			if ((Train + i)->Free < (Train + j)->Free) {
				Database st = Train[i];
				Train[i] = Train[j];
				Train[j] = st;
			}
	for (int i = 0; i < n; i++) {
		if (!strcmp((Train + i)->Destination, "Brest")) {
			kol++;
			Out(i);
		}
	}
}

void main() {
	int i, n, kol = 0;
	cout << "\n Number of trains = ";
	cin >> n;
	Train = new Database[n];
	In(n);
	cout << "\n\n Train Information: \n";
	for (i = 0; i < n; i++) Out(i);
	cout << "\n\n Destination: 'Brest': ";
	Poisk(Train, n, kol);
	cout << "\n\n Found trains: " << kol << endl;
	delete[] Train;
	cout << "\n\n";
}