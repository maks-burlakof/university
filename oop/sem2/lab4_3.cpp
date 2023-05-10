// Кассовое обслуживание банка. В кассовой зоне банка имеется несколько касс. В одной кассе
//обслуживается несколько видов операций, но транзакции должны иметь каждая свою очередь для
//фиксации и записи в системе. Организовать работу касс банка.

#include <iostream>
#include <string>
#include <thread>
#include <mutex>
#include <chrono>

using namespace std;

const int NUM_CASH_REGISTERS = 2;  // число касс
const int NUM_TRANSACTION_TYPES = 3;  // количество типов транзакций

class Bank {
private:
    int cash_registers[NUM_CASH_REGISTERS][NUM_TRANSACTION_TYPES] = {0};
    mutex mtx;
public:
    Bank() {}

    void create_transactions() {
        int transactions_num;
        printmsg("Начало рабочей смены!");
        for (int i = 0; i < NUM_CASH_REGISTERS; i++) {
            for (int j = 0; j < NUM_TRANSACTION_TYPES; j++) {
                transactions_num = rand() % 3 + 1;
                mtx.lock();
                cash_registers[i][j] = transactions_num;
                mtx.unlock();
                printmsg("Добавлено " + to_string(transactions_num) + " транзакций типа " + to_string(j+1) + " в кассу #" +
                                 to_string(i+1));
                this_thread::sleep_for(chrono::seconds(3));
            }
        }
        printmsg("Конец рабочей смены!");
    }

    void process_cash_register(int register_index) {
        int completion_time;
        while (true) {
            for (int i = 1; i <= NUM_TRANSACTION_TYPES; i++) {
                mtx.lock();
                if (cash_registers[register_index][i] > 0) {
                    completion_time = rand() % 7 + 1;
                    cout << "Обработка транзакции типа " << i << " в кассе # " << register_index << endl;
                    mtx.unlock();
                    this_thread::sleep_for(chrono::seconds(completion_time));
                    mtx.lock();
                    cash_registers[register_index][i]--;
                    cout << "Транзакция типа " << i << " обработана в кассе " << register_index << " за " << completion_time << " секунд...\n";
                }
                mtx.unlock();
            }
        }
    }

    void printmsg(string message) {
        mtx.lock();
        cout << message << endl;
        mtx.unlock();
    }
};

int main() {
    thread threads[NUM_CASH_REGISTERS];
    Bank bank;
    for (int i = 0; i < NUM_CASH_REGISTERS; i++) {
        threads[i] = thread(&Bank::process_cash_register, &bank, i+1);
    }

    // Добавляем транзакции в каждую кассу
    thread(&Bank::create_transactions, &bank).join();

    // Ждем выполнение всех потоков
    for (int i = 0; i < NUM_CASH_REGISTERS; i++) {
        threads[i].join();
    }

    return 0;
}
