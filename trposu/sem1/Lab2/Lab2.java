import java.util.Scanner;

public class Lab2 {
    private int id;
    private String lastName;
    private String firstName;
    private String secondName;
    private String address;
    private String phone;
    private int medicalRecordNumber;
    private String diagnosis;

    public Lab2(int id, String lastName, String firstName, String secondName, String address, String phone, int medicalRecordNumber, String diagnosis) {
        this.id = id;
        this.lastName = lastName;
        this.firstName = firstName;
        this.secondName = secondName;
        this.address = address;
        this.phone = phone;
        this.medicalRecordNumber = medicalRecordNumber;
        this.diagnosis = diagnosis;
    }

    public void setType(String diagnosis) {
        this.diagnosis = diagnosis;
    }

    public String getType() {
        return this.diagnosis;
    }

    public String toString() {
        return "ID: " + this.id + ", Last Name: " + this.lastName + ", First Name: " + this.firstName + ", Second Name: " + this.secondName + ", Address: " + this.address + ", Phone: " + this.phone + ", Medical Record Number: " + this.medicalRecordNumber + ", Diagnosis: " + this.diagnosis;
    }

    public static Lab2[] createPatients() {
        Lab2[] patients = new Lab2[8];
        patients[0] = new Lab2(1, "Иванов", "Иван", "Иванович", "ул. Ленина 1, Минск", "+375(29)876-16-15", 12345, "Грипп");
        patients[1] = new Lab2(2, "Сидорова", "Елена", "Петровна", "ул. Строителей 2, Гомель", "+375(33)234-56-78", 23456, "Артрит");
        patients[2] = new Lab2(3, "Петров", "Алексей", "Сергеевич", "ул. Молодежная 3, Брест", "+375(44)786-15-67", 34567, "Бронхит");
        patients[3] = new Lab2(4, "Коваленко", "Оксана", "Александровна", "ул. Советская 4, Витебск", "+375(29)768-12-08", 45678, "Артрит");
        patients[4] = new Lab2(5, "Григорьева", "Анна", "Александровна", "ул. Ленина 6, Минск", "+375(29)123-45-67", 78956, "Гастрит");
        patients[5] = new Lab2(6, "Козлов", "Андрей", "Васильевич", "ул. Первомайская 2, Гомель", "+375(33)234-56-78", 15705, "Грипп");
        patients[6] = new Lab2(7, "Павлова", "Наталья", "Сергеевна", "ул. Советская 4, Брест", "+375(44)777-00-12", 70901, "Грипп");
        patients[7] = new Lab2(8, "Ковалев", "Владимир", "Игоревич", "ул. Социалистическая 3, Витебск", "+375(29)956-19-78", 74071, "Гастрит");
        return patients;
    }

    public static void printPatientsByDiagnosis(Lab2[] patients, String diagnosis) {
        for (Lab2 patient : patients) {
            if (patient.getType().equals(diagnosis)) {
                System.out.println(patient.toString());
            }
        }
    }

    public static void printPatientsByMedicalRecordNumber(Lab2[] patients, int start, int end) {
        for (Lab2 patient : patients) {
            if (patient.medicalRecordNumber >= start && patient.medicalRecordNumber <= end) {
                System.out.println(patient.toString());
            }
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Lab2[] patients = Lab2.createPatients();

        System.out.print("Enter a diagnosis to search: ");
        String diagnosisInput = scanner.nextLine().trim();
        String diagnosis = diagnosisInput.substring(0, 1).toUpperCase() + diagnosisInput.substring(1);
        Lab2.printPatientsByDiagnosis(patients, diagnosis);

        System.out.print("\nEnter a range of medical record number (separated by spaces): ");
        int start = scanner.nextInt();
        int end = scanner.nextInt();
        Lab2.printPatientsByMedicalRecordNumber(patients, start, end);
    }
}
