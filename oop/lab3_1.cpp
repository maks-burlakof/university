#include <iostream>
#include <conio.h>
#include <Windows.h>
#include "ChipHeader.h"
using namespace std;

Type* addElement(Type*, int);
void fillArray(Type*, int, int);
int input();

int main() {
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);
	setlocale(LC_ALL, "Russian");

	int n = 0, choice;
	
	cout << "Введите число элементов:\n >>> ";
	cin >> n;
	Type* chips = new Type[n];
	fillArray(chips, 0, n);
	while (true) {
	    cout << "\n~~~~~~~~~~ МЕНЮ ~~~~~~~~~~\n "
	        "1 - Добавить объект\n "
	        "2 - Просмотр текущего состояния объектов\n "
			"3 - Список микросхем указанной ёмкости\n"
	        "0 - ВЫХОД\n";
	    switch (_getch()) {
		case '1': {  // Создаем область видимости
			system("cls");
			chips = addElement(chips, n);
			n++;
			break;
		}
		case '2': {
			system("cls");
			if (n == 0) {
				cout << "Для просмотра объектов сначала создайте их.\n";
				break;
			}
			cout << "Найдено записей: " << n << "\n"
				"Введите порядковый номер для просмотра объекта.\n"
				"Для просмотра всех объектов введите '0'\n >>> ";
			choice = input();

			if (choice != 0) {
				while (choice < 1 || choice > n) {
					cout << "Введенное значение превышает количество записей.\n"
						"Повторите попытку:\n >>> ";
					choice = input();
				}
				chips[--choice].print();
			}
			else {
				for (int i = 0; i < n; i++) {
					cout << i+1 << ".\n";
					chips[i].print();
				}
			}
			break;
		}
		case '3': {
			cout << "Введите требуемую ёмкость:\n >>> ";
			int cap = input();
			for (int i = 0; i < n; i++) chipList(cap, chips[i]);
			break;
		}
	    case '0':
	        system("cls");
			delete[] chips;
	        return 0;
	    default:
	        // system("cls");
	        break;
	    }
	}
	return 0;
}


Type* addElement(Type* massiv, int number) {
	int numTemp = number + 1;
	Type* temp = new Type[numTemp];
	for (int i = 0; i < number; i++) temp[i] = massiv[i];
	fillArray(temp, number, numTemp);
	delete[] massiv;
	return temp;
}


void fillArray(Type* massiv, int start, int end) {
	char name[81], type[81], sort[81], interface_type[81], manufacture_date[81], factory_name[81], status[81];
	int capacity;
	for (int i = start; i < end; i++) {
		cout << i+1 << ".\n";
		cout << "Наименование:\n >>> ";
		cin >> name;
		cout << "Тип памяти (оперативная, постоянная):\n >>> ";
		cin >> type;
		if (!strcmp(type, "оперативная") || !strcmp(type, "Оперативная")) {
			cout << "Вид (статическая/динамическая):\n >>> ";
			cin >> sort;
		}
		else {
			if (!strcmp(type, "постоянная") || !strcmp(type, "Постоянная")) {
				cout << "Вид (с электрическим стиранием/с ультрафиолетовым стиранием):\n >>> ";
				cin >> sort;
			}
			else strcpy_s(sort, "");
		}
		
		cout << "Информационная ёмкость:\n >>> ";
		capacity = input();
		cout << "Интерфейс (последовательная/параллельная память):\n >>> ";
		cin >> interface_type;
		cout << "Год/месяц даты производства:\n >>> ";
		cin >> manufacture_date;
		cout << "Фирма/завод-производитель:\n >>> ";
		cin >> factory_name;
		cout << "Статус (новая/использованная):\n >>> ";
		cin >> status;
		massiv[i] = Type(name, type, sort, capacity, interface_type, manufacture_date, factory_name, status);
	}
}


int input() {
	int in;
	while (!(cin >> in)) {
		cout << "Введенное значение должно быть целым числом! Повторите попытку.\n >>> ";
		cin.clear();
		while (cin.get() != '\n');
	}
	return in;
}
