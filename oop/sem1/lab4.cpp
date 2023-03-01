#include <iostream>
#include <conio.h>
#include <Windows.h>
#include "TemplateHeader.h"
using namespace std;

int main() {
	SetConsoleCP(1251);
	SetConsoleOutputCP(1251);
	setlocale(LC_ALL, "Russian");
	
	int n, num;
	cout << "Введите число элементов N:\n >> ";
	n = input(true);
	
	// Здесь можно изменять типы данных (Type | ResultType)
	List <bool, double> arr(n);

	while (true) {
		cout << "\n~~~~~~~~~~~~~~~~~~~~ МЕНЮ ~~~~~~~~~~~~~~~~~~~~\n "
			"1 - Просмотр текущего состояния объектов\n "
			"2 - Инициализация n объектов с начала массива\n "
			"3 - Инициализация объекта с запросом номера\n "
			"4 - Удаление заданного объекта\n "
			"5 - Формирование массива по алгоритму\n "
			"0 - ВЫХОД\n";
		
		switch (_getch()) {
		case '1':
			system("cls");
			arr.print();
			break;
		case '2':
			system("cls");
			cout << "Заполните массив из " << n << " элементов:\n";
			arr.set();
			break;
		case '3':
			system("cls");
			cout << "Исходный массив:\n";
			arr.print();
			cout << "Введите номер элемента для инициализации: \n >> ";
			num = input(true);
			arr.set(num);
			n = max(n, num);
			break;
		case '4':
			system("cls");
			cout << "Исходный массив:\n";
			arr.print();
			cout << "Введите номер элемента для удаления: \n >> ";
			arr.remove(input(true, n));
			n--;
			break;
		case '5':
			system("cls");
			arr.task();
			break;
		case '0':
			system("cls");
			return 0;
		default:
			break;
		}
	}
	return 0;
}
