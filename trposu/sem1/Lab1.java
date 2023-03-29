import java.util.Arrays;
import java.util.Collections;
import java.util.Scanner;

public class Lab1 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Enter numbers separated by spaces: ");
        String line = scanner.nextLine();
        String[] numbers = line.split(" ");
        Collections.reverse(Arrays.asList(numbers));

        int[] lengths = new int[numbers.length];
        for (int i = 0; i < numbers.length; i++) {
            lengths[i] = numbers[i].length();
        }

        double averageLength = Arrays.stream(lengths).average().orElse(0);

        int[] shorterNumbers = Arrays.stream(numbers)
                .filter(number -> number.length() < averageLength)
                .mapToInt(Integer::parseInt)
                .toArray();

        int[] longerNumbers = Arrays.stream(numbers)
                .filter(number -> number.length() > averageLength)
                .mapToInt(Integer::parseInt)
                .toArray();

        System.out.println("Numbers with length less than average:");
        for (int number : shorterNumbers) {
            System.out.printf("%d (%d)%n", number, String.valueOf(number).length());
        }

        System.out.println("Numbers with length greater than average:");
        for (int number : longerNumbers) {
            System.out.printf("%d (%d)%n", number, String.valueOf(number).length());
        }

        System.out.print("Developed by Maksim Burlakov, received 02/09/2023, assignment date 03/11/2023");
    }
}
