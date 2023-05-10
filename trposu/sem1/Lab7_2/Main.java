package Lab7_2;

import java.sql.*;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        try {
            Taxpayer person = new Taxpayer("Иван Гришаёнок", "34571-1234-09", 13, "incomes.db");
            System.out.println("Подключено к базе данных!");
            System.out.println("Налогоплательщик: " + person);
            System.out.println("Ставка подоходного налога: " + person.getTaxValue() + "%");
            person.createTablesIfNotExist();

            Scanner scanner = new Scanner(System.in);
            boolean is_exit = false;
            while (true) {
                if (is_exit) {
                    break;
                }
                System.out.println("\n----- Main Menu -----");
                System.out.println("1. Просмотр\n2. Добавить\n3. Удалить\n4. Посчитать\n0. EXIT");
                String choice = scanner.nextLine();
                switch (choice) {
                    case "1":
                        System.out.println("Incomes:");
                        List<String> incomes = person.viewIncomes();
                        for (String income : incomes) {
                            System.out.println(income);
                        }
                        break;
                    case "2":
                        Scanner scanner_ = new Scanner(System.in);
                        System.out.println("Введите тип дохода: ");
                        String type = scanner_.nextLine();
                        System.out.println("Введите величину дохода: ");
                        double amount = 0;
                        while (true) {
                            if (scanner_.hasNextDouble()) {
                                amount = scanner_.nextDouble();
                                break;
                            } else {
                                System.out.println("Неверный ввод, ожидается дробное число. Попробуйте еще раз.");
                                scanner_.nextLine();
                            }
                        }
                        Income income = new Income(amount, type);
                        person.addIncome(income);
                        break;
                    case "3":
                        Scanner scanner_2 = new Scanner(System.in);
                        System.out.println("Введите id записи: ");
                        String id = scanner_2.nextLine();
                        person.deleteIncome(id);
                        break;
                    case "4":
                        String income_amount = person.calculateTotalIncomes();
                        System.out.println("Итоговый доход: " + income_amount + " р.");
                        System.out.println("Итоговый налоговый вычет: " + person.calculateTotalTax(income_amount) + " р.");
                        break;
                    case "0":
                        is_exit = true;
                        break;
                    default:
                        System.out.println("Invalid input. Please enter a number.");
                }
            }
        } catch (SQLException e) {
            System.err.println("Error: " + e.getMessage());
        }
    }
}
