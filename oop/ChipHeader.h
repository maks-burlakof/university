/*
Создать программу с классом Chip, порождающим объекты – данные о микросхемах памяти, хранящиеся на складе.
Класс включает в себя следующие поля и методы:
- тип (оперативная, постоянная);
- информационная ёмкость;
- наименование;
- интерфейс (последовательная/параллельная память);
- год/месяц даты производства;
- фирма/завод-производитель;

- конструктор по умолчанию;
- деструктор;
- метод инициализации текущего состояния объектов;
- функция-друг, выводящая список микросхем, указанной информационной ёмкости;
- виртуальный метод просмотра текущего объекта print().

Производный класс Type имеет следующие элементы:
- вид (для оперативной памяти – статическая/динамическая; для постоянной – с электрическим стиранием/с ультрафиолетовым);
- статус (новая/использованная);
- виртуальный метод просмотра состояния объектов.
*/


#pragma once
#include <iostream>

using namespace std;

class Chip {
public:
	char name[81];
	char type[81];
	int capacity;
	char interface_type[81];
	char manufacture_date[81];
	char factory_name[81];

	friend void chipList(int, Chip&);

	Chip() {
		strcpy_s(name, "");
		strcpy_s(type, "");
		capacity = 0;
		strcpy_s(interface_type, "");
		strcpy_s(manufacture_date, "");
		strcpy_s(factory_name, "");
	}

	Chip(char *n, char* t, int c, char* i, char* m, char* f) {
		strcpy_s(name, n);
		strcpy_s(type, t);
		capacity = c;
		strcpy_s(interface_type, i);
		strcpy_s(manufacture_date, m);
		strcpy_s(factory_name, f);
	}

	// Метод инициализации текущего состояния объектов??

	virtual void print() {
		cout << "Наименование: " << name << "\n"
			"Тип памяти: " << type << "\n"
			"Информационная ёмкость: " << capacity << "\n"
			"Интерфейс памяти: " << interface_type << "\n"
			"Год/месяц даты производства: " << manufacture_date << "\n"
			"Фирма/завод-производитель: " << factory_name << "\n";
	}

	~Chip() {
		cout << "Деструктор вызван для объекта '" << name << "'\n";
	}
};


void chipList(int cap, Chip& self) {
	int n = 0;
	if (self.capacity == cap) {
		cout << ++n << ".\n";
		self.print();
	}
}


class Type : public Chip {
public:
	char sort[81];
	char status[81];

	Type() :Chip() {
		strcpy_s(sort, "");
		strcpy_s(status, "");
	}

	Type(char* n, char* t, char* sor, int c, char* i, char* m, char* f, char* stat) :Chip(n, t, c, i, m, f) {
		strcpy_s(sort, sor);
		strcpy_s(status, stat);
	}

	void print() {
		cout << "Наименование: " << name << "\n"
			"Тип памяти: " << type << "\n"
			"Вид: " << sort << "\n"
			"Информационная ёмкость: " << capacity << "\n"
			"Интерфейс памяти: " << interface_type << "\n"
			"Год/месяц даты производства: " << manufacture_date << "\n"
			"Фирма/завод-производитель: " << factory_name << "\n"
			"Статус: " << status << "\n";
	}

	~Type() {
		cout << "Деструктор вызван для объекта '" << name << "'\n";
	}
};