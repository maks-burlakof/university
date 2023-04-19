#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>

using namespace std;

class Hypermarket {
private:
    int available_checkouts, max_wait;
    mutex market_mutex;
public:
    Hypermarket(int num_ckeckouts, int max_waiting_time) {
        available_checkouts = num_ckeckouts;
        max_wait = max_waiting_time;
    }

    void check_out(int customer_id) {
        bool stayed = false;
        int temporary_time;

        while (!stayed) {
            market_mutex.lock();
            if (available_checkouts > 0) {
                available_checkouts--;
                temporary_time = rand() % max_wait + 1;
                cout << "Customer " << customer_id << " has stayed. Staying for " << temporary_time << " seconds. Available checkouts: " << available_checkouts << endl;
                market_mutex.unlock();
                this_thread::sleep_for(chrono::seconds(temporary_time));
                market_mutex.lock();
                available_checkouts++;
                cout << "Customer " << customer_id << " has left. Available checkouts: " << available_checkouts << endl;
                stayed = true;
                market_mutex.unlock();
            }
            else {
                temporary_time = rand() % max_wait + 1;
                cout << "Customer " << customer_id << " cannot stay. Waiting for " << temporary_time << " seconds..." << endl;
                market_mutex.unlock();
                this_thread::sleep_for(chrono::seconds(temporary_time));
            }
        }
    }
};

int main() {
    const int NUM_CUSTOMERS = 10;
    const int NUM_CHECKOUTS = 5;
    const int MAX_TIME = 10;

    thread customers[NUM_CUSTOMERS];
    Hypermarket market(NUM_CHECKOUTS, MAX_TIME);

    for (int i = 0; i < NUM_CUSTOMERS; i++) {
        customers[i] = thread(&Hypermarket::check_out, &market, i + 1);
    }

    for (auto & customer : customers) {
        customer.join();
    }

    return 0;
}
