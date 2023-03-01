#pragma once
using namespace std;

double input(bool, int);

template <class Type, class ResultType>
class List {
private:
	int n;
	Type* arr;
	ResultType* task_arr;
public:
	List() {
		arr = new Type[0];
		n = 0;
	}

	List(int num) {
		arr = new Type[num];
		n = num;
	}
	
	~List() {
		delete[] arr;
		delete[] task_arr;
	}

	void set() {
		for (int i = 0; i < n; i++) {
			cout << "#" << i + 1 << ":\n >> ";
			cin >> arr[i];
		}
	}

	void set(int num) {
		if (num > n) {
			cout << "Массив будет расширен, так как введенное значение превышает исходный размер.\n";
			arr = addElement(num);
			int n_old = n;
			n = num;
			cout << "#" << num << ":\n >> ";
			cin >> arr[num - 1];
			if (num - n_old > 1) {
				cout << "Инициализировать также элемент(-ы)";
				for (int i = n_old + 1; i < num; i++)
					cout << " #" << i;
				cout << "?\n (y/n)\n";
				if (_getch() == 'y')
					for (int i = n_old + 1; i < num; i++)
						set(i);
			}
		}
		else {
			cout << "#" << num << ":\n >> ";
			cin >> arr[num - 1];
		}
	}

	Type* addElement(int num) {
		Type* tempArr = new Type[num];
		for (int i = 0; i < n; i++) tempArr[i] = arr[i];
		return tempArr;
	}

	void remove(int num) {
		cout << "Элемент " << arr[num - 1] << " с индексом " << num << " удалён.";
		for (int i = num - 1; i < n-1; i++) {
			arr[i] = arr[i + 1];
		}
		n--;
	}

	void print() {
		for (int i = 0; i < n; i++) {
			cout << "|" << i + 1 << "|" << arr[i] << "\n";
		}
	}
	
	void task() {
		task_arr = new ResultType[n];

		cout << "     Исходный\t\tМассив, созданный\n массив объектов\t  по алгоритму\n\n";

		for (int i = 0; i < n; i++) {
			ResultType sum = 0;
			for (int j = 0; j <= i; j++)
				sum += arr[j];
			task_arr[i] = abs(sum);
			cout << " |" << i + 1 << "|" << arr[i] << "\t\t";
			cout << " |" << i + 1 << "|" << task_arr[i] << "\n";
		}
	}
};

double input(bool is_positive=false, int max_val=0) {
	// При is_positive = True отрицательные элементы и 0 вводить нельзя
	// При заданном max_val больше этого значения вводить нельзя
	double in;
	while (!(cin >> in) || (is_positive && in <= 0) || (max_val && in > max_val)) {
		cout << "Недействительное значение! Повторите попытку.\n >> ";
		cin.clear();
		while (cin.get() != '\n');
	}
	return in;
}