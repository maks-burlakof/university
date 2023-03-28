#include <iostream>
#include <thread>
#include <mutex>
#include <chrono>

using namespace std;

class Parking {
private:
    int available_places, max_wait;
    mutex parking_mutex;
public:
    Parking(int num_places, int max_waiting_time) {
        available_places = num_places;
        max_wait = max_waiting_time;
    }

    void park_car(int car_id) {
        bool parked = false;
        int temporary_time;

        while (!parked) {
            parking_mutex.lock();
            if (available_places > 0) {
                available_places--;
                temporary_time = rand() % max_wait + 1;
                cout << "Car " << car_id << " has parked. Parking for " << temporary_time << " seconds. Available spaces: " << available_places << endl;
                parking_mutex.unlock();
                this_thread::sleep_for(chrono::seconds(temporary_time));
                parking_mutex.lock();
                available_places++;
                cout << "Car " << car_id << " has left. Available spaces: " << available_places << endl;
                parked = true;
                parking_mutex.unlock();
            }
            else {
                temporary_time = rand() % max_wait + 1;
                cout << "Car " << car_id << " cannot park. Waiting for " << temporary_time << " seconds..." << endl;
                parking_mutex.unlock();
                this_thread::sleep_for(chrono::seconds(temporary_time));
            }
        }
    }
};

int main() {
    const int NUM_CARS = 10;
    const int NUM_SPACES = 5;
    const int MAX_TIME = 10;

    thread cars[NUM_CARS];
    Parking parking(NUM_SPACES, MAX_TIME);

    for (int i = 0; i < NUM_CARS; i++) {
        cars[i] = thread(&Parking::park_car, &parking, i+1);
    }

    for (auto & car : cars) {
        car.join();
    }
    return 0;
}
