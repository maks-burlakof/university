import java.util.Scanner;

public class Lab2_2 {
    private String destination;
    private int flightNumber;
    private String typeOfPlane;
    private String departureTime;
    private String daysOfWeek;

    public Lab2_2(String destination, int flightNumber, String typeOfPlane, String departureTime, String daysOfWeek) {
        this.destination = destination;
        this.flightNumber = flightNumber;
        this.typeOfPlane = typeOfPlane;
        this.departureTime = departureTime;
        this.daysOfWeek = daysOfWeek;
    }

    public String getDestination() { return destination; }
    public String getDepartureTime() { return departureTime; }
    public String getDaysOfWeek() { return daysOfWeek; }

    public String toString() {
        return "Number: " + this.flightNumber + "; Type: " + this.typeOfPlane + "; Destination: " + destination +
                "; Departure time: " + this.departureTime + "; Week days: " + this.daysOfWeek;
    }

    public static Lab2_2[] createAirlines() {
        return new Lab2_2[]{
                new Lab2_2("New York", 101, "Boeing 747", "08:00", "Monday"),
                new Lab2_2("Los Angeles", 202, "Airbus A380", "12:00", "Tuesday, Thursday"),
                new Lab2_2("Miami", 303, "Boeing 777", "15:30", "Wednesday, Friday, Sunday"),
                new Lab2_2("Chicago", 404, "Boeing 787", "18:45", "Monday, Friday"),
                new Lab2_2("Dallas", 505, "Airbus A350", "20:15", "Tuesday, Thursday, Saturday"),
                new Lab2_2("New York", 557, "Boeing 737", "12:30", "Monday, Wednesday, Friday"),
                new Lab2_2("Los Angeles", 543, "Airbus A320", "14:45", "Monday, Thursday, Saturday"),
                new Lab2_2("Chicago", 432, "Boeing 787", "16:20", "Tuesday, Friday, Sunday"),
                new Lab2_2("Miami", 123, "Airbus A321", "18:15", "Monday, Wednesday, Friday, Sunday"),
                new Lab2_2("Seattle", 678, "Boeing 737", "20:30", "Tuesday, Thursday, Saturday"),
                new Lab2_2("Dallas", 574, "Airbus A320", "10:00", "Monday, Wednesday, Friday, Sunday"),
                new Lab2_2("San Francisco", 568, "Boeing 777", "11:45", "Tuesday, Thursday, Saturday"),
                new Lab2_2("Boston", 158, "Boeing 737", "13:10", "Monday, Wednesday, Friday, Sunday"),
                new Lab2_2("Las Vegas", 592, "Airbus A320", "15:30", "Tuesday, Thursday, Saturday"),
                new Lab2_2("Orlando", 401, "Boeing 737", "17:25", "Monday, Wednesday, Friday"),
                new Lab2_2("Houston", 406, "Airbus A321", "19:40", "Tuesday, Thursday, Saturday"),
                new Lab2_2("Denver", 193, "Boeing 737", "21:15", "Monday, Wednesday, Friday, Sunday")
        };
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Lab2_2[] airlines = Lab2_2.createAirlines();

        // Output the list of flights for a given destination
        System.out.print("Enter destination: ");
        String destination = scanner.nextLine();
        System.out.println("Flights to " + destination + ":");
        for (Lab2_2 airline : airlines) {
            if (airline.getDestination().equalsIgnoreCase(destination)) {
                System.out.println(airline);
            }
        }

        // Output the list of flights for a given day of the week
        System.out.print("\nEnter day of the week: ");
        String dayOfWeek = scanner.nextLine();
        System.out.println("Flights on " + dayOfWeek + ":");
        for (Lab2_2 airline : airlines) {
            if (airline.getDaysOfWeek().toLowerCase().contains(dayOfWeek.toLowerCase())) {
                System.out.println(airline);
            }
        }

        // Output the list of flights for a given day of the week, for which the departure time is longer than the given one
        System.out.print("\nEnter departure time (HH:MM): ");
        String departureTime = scanner.nextLine();
        System.out.println("Flights on " + dayOfWeek + " with departure time later than " + departureTime + ":");
        for (Lab2_2 airline : airlines) {
            if (airline.getDaysOfWeek().toLowerCase().contains(dayOfWeek.toLowerCase()) && airline.getDepartureTime().compareTo(departureTime) > 0) {
                System.out.println(airline);
            }
        }
    }
}
