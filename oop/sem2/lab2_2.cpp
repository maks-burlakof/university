#include <iostream>
#include <string>

using namespace std;

class Airline {
private:
    string destination, number, type, departureTime, weekDays;

public:
    Airline() {}

    Airline(string _number, string _type, string _destination, string _departureTime, string _weekDays) {
        number = _number;
        type = _type;
        destination = _destination;
        departureTime = _departureTime;
        weekDays = _weekDays;
    }

    string getDestination() {
        return destination;
    }

    bool is_weekDay(string weekDay) {
        bool is_find = false;
        for (char i : weekDays) {
            if (weekDay[0] == i) {
                is_find = true;
                break;
            }
        }
        return is_find;
    }

    bool is_timeGreater(string minDepartureTime) {
        int minHour = stoi(minDepartureTime.substr(0, 2));
        int minMinute = stoi(minDepartureTime.substr(3, 2));
        int Hour = stoi(departureTime.substr(0, 2));
        int Minute = stoi(departureTime.substr(3, 2));
        if (minHour < Hour) {
            return true;
        }
        else {
            if (minHour == Hour and minMinute < Minute ) {
                return true;
            } else {
                return false;
            }
        }
    }

    string toString() {
        return "Number: " + number + "; Type: " + type + "; Destination: " + destination +
               "; Departure time: " + departureTime + "; Week days: " + weekDays + "\n";
    }
};

void printAirlinesByDestination(Airline airlines[], int size, string destination) {
    for (int i = 0; i < size; i++) {
        if (airlines[i].getDestination() == destination) {
            cout << airlines[i].toString();
        }
    }
}

void printAirlinesByWeekDay(Airline airlines[], int size, string weekDay) {
    for (int i = 0; i < size; i++) {
        if (airlines[i].is_weekDay(weekDay)) {
            cout << airlines[i].toString();
        }
    }
}

void printAirlinesByDepartureTime(Airline airlines[], int size, string weekDay, string minDepartureTime) {
    for (int i = 0; i < size; i++) {
        if (airlines[i].is_weekDay(weekDay) & airlines[i].is_timeGreater(minDepartureTime)) {
            cout << airlines[i].toString();
        }
    }
}

int main() {
    const int n = 9;
    Airline airlines[n];
    airlines[0] = Airline("B2 727", "Boeing 737-800", "Дубай", "00:50", "4,5,6");
    airlines[1] = Airline("B2 975", "Embraer 195", "Москва", "08:45", "1,2,3,4,5,6,7");
    airlines[2] = Airline("B2 941", "Embraer 195", "Санкт-Петербург", "09:20", "1,3,4,5,6");
    airlines[3] = Airline("B2 783", "Boeing 737-800", "Стамбул", "18:25", "1,7");
    airlines[4] = Airline("B2 775", "Embraer 195", "Астана", "20:15", "1,3,5");
    airlines[5] = Airline("B2 735", "Boeing 737-800", "Тбилиси", "22:50", "3,7");
    airlines[6] = Airline("B2 737", "Embraer 195", "Батуми", "23:20", "2,4,6");
    airlines[7] = Airline("B2 123", "Airbus A380", "Нью-Йорк", "10:45", "5");
    airlines[8] = Airline("B2 346", "Boeing 767-33A", "Рим", "13:00", "1,2,3,4,5,6,7");

    string destination;
    cout << "Enter a destination: ";
    cin >> destination;
    printAirlinesByDestination(airlines, n, destination);

    string weekDay;
    cout << "\nEnter the number of the day of the week: ";
    cin >> weekDay;
    printAirlinesByWeekDay(airlines, n, weekDay);

    string minDepartureTime;
    cout << "\nEnter the minimum departure time: ";
    cin >> minDepartureTime;
    printAirlinesByDepartureTime(airlines, n, weekDay, minDepartureTime);

    return 0;
}