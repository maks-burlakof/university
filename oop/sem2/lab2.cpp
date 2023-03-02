#include <iostream>
#include <string>

using namespace std;

class Patient {
private:
    int id;
    string lastName, firstName, secondName, address, phone, diagnosis;
    int medicalRecordNumber;

public:
    Patient() {}

    Patient(int _id, string _lastName, string _firstName, string _secondName, string _address, string _phone,
            int _medicalRecordNumber, string _diagnosis) {
        id = _id;
        lastName = _lastName;
        firstName = _firstName;
        secondName = _secondName;
        address = _address;
        phone = _phone;
        medicalRecordNumber = _medicalRecordNumber;
        diagnosis = _diagnosis;
    }

    int getMedicalRecordNumber() {
        return medicalRecordNumber;
    }
    string getDiagnosis() {
        return diagnosis;
    }

    void setType(int id) {
        this->id = id;
    }

    string toString() {
        string str = "ID: " + to_string(id) + "; Last Name: " + lastName + "; First Name: " + firstName +
                "; Second Name: " + secondName + "; Address: " + address + "; Phone: " + phone +
                "; Medical Record Number: " + to_string(medicalRecordNumber) + "; Diagnosis: " + diagnosis + "\n";
        return str;
    }
};

void printPatientsByDiagnosis(Patient patients[], int size, string diagnosis) {
    cout << "Patients with Diagnosis " << diagnosis << ":" << endl;
    for (int i = 0; i < size; i++) {
        if (patients[i].getDiagnosis() == diagnosis) {
            cout << patients[i].toString();
        }
    }
}

void printPatientsByMedicalRecordNumber(Patient patients[], int size, int minMedicalRecordNumber, int maxMedicalRecordNumber) {
    cout << "Patients with Medical Record Number in the range [" << minMedicalRecordNumber << ", "
         << maxMedicalRecordNumber << "]:\n";
    for (int i = 0; i < size; i++) {
        int medicalRecordNumber = patients[i].getMedicalRecordNumber();
        if (medicalRecordNumber >= minMedicalRecordNumber && medicalRecordNumber <= maxMedicalRecordNumber) {
            cout << patients[i].toString();
        }
    }
}

int main() {
    Patient patients[8];
    patients[0] = Patient(1, "Иванов", "Иван", "Иванович", "ул. Ленина 1, Минск", "+375(29)876-16-15", 12345, "Грипп");
    patients[1] = Patient(2, "Сидорова", "Елена", "Петровна", "ул. Строителей 2, Гомель", "+375(33)234-56-78", 23456, "Артрит");
    patients[2] = Patient(3, "Петров", "Алексей", "Сергеевич", "ул. Молодежная 3, Брест", "+375(44)786-15-67", 34567, "Бронхит");
    patients[3] = Patient(4, "Коваленко", "Оксана", "Александровна", "ул. Советская 4, Витебск", "+375(29)768-12-08", 45678, "Артрит");
    patients[4] = Patient(5, "Григорьева", "Анна", "Александровна", "ул. Ленина 6, Минск", "+375(29)123-45-67", 78956, "Гастрит");
    patients[5] = Patient(6, "Козлов", "Андрей", "Васильевич", "ул. Первомайская 2, Гомель", "+375(33)234-56-78", 15705, "Грипп");
    patients[6] = Patient(7, "Павлова", "Наталья", "Сергеевна", "ул. Советская 4, Брест", "+375(44)777-00-12", 70901, "Грипп");
    patients[7] = Patient(8, "Ковалев", "Владимир", "Игоревич", "ул. Социалистическая 3, Витебск", "+375(29)956-19-78", 74071, "Гастрит");

    string diagnosis;
    cout << "Enter a diagnosis to search: ";
    cin >> diagnosis;
    printPatientsByDiagnosis(patients, 8, diagnosis);

    int start, end;
    cout << "\nEnter a range of medical record number (separated by spaces): ";
    cin >> start >> end;
    printPatientsByMedicalRecordNumber(patients, 8, start, end);

    return 0;
}